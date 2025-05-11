import os
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    APIKeyHeader,
    OAuth2PasswordRequestForm,
)
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from wasabi import msg
from dotenv import load_dotenv

load_dotenv()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    idm_role: str
    disabled: Optional[bool] = None
    hashed_password: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    idm_role: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

oauth2_scheme = APIKeyHeader(name="API-Key", auto_error=False)

DATABASE = {
    "tim": {
        "username": "tim",
        "full_name": "Tim Ruscica",
        "email": "tim@gmail.com",
        "idm_role": "Viewer",
        "hashed_password": "$2b$12$HxWHkvMuL7WrZad6lcCfluNFj1/Zp63lvP5aUrKlSTYtoFzPXHOtu",
        "disabled": False,
    }
}


class GenAccToken:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self) -> None:

        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.authenticate_user(
            username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data=user.model_dump(),
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user(self, db=None, token_data: str = None):
        if db is not None and isinstance(token_data, str):
            if token_data in db:
                token_data = db[token_data]
                return UserInDB(**token_data)
            else:
                return None  # User not found in the database

        elif isinstance(token_data, dict):
            token_data = token_data
            return UserInDB(**token_data)
        else:
            raise ValueError(
                "Invalid input: Either 'db' and 'token_data' (str) or 'token_data' (dict) must be provided."
            )

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(db=DATABASE, token_data=username)
        # if not user:
        #     return False
        # if not self.verify_password(password, user.hashed_password):
        #     return False
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        """
        Retrieves the current user based on the provided authentication token.
        Args:
            token (str): The OAuth2 bearer token provided in the request header.
        Returns:
            User: The authenticated user object.
        Raises:
            HTTPException: If the token is invalid, expired, or the user cannot be authenticated.
        Notes:
            - The token is decoded using the specified secret key and algorithm.
            - The payload must contain "username" and "idm_role" fields.
            - If the user cannot be retrieved from the database, an exception is raised.
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[self.ALGORITHM])

            username: str = payload.get("username")
            idm_role: str = payload.get("idm_role")
            if username is None or idm_role is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Can not validate username or idm_role",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token_data = TokenData(**payload)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="JWTError",
                headers={"WWW-Authenticate": "Bearer"},
            )

        current_user = self.get_user(db=None, token_data=token_data.model_dump())
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Can not validate current user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return current_user

    @staticmethod
    def get_user(db: dict = None, token_data: str = None) -> UserInDB:
        """
        Retrieves a user from a database or a dictionary.

        Args:
            db (dict, optional): A dictionary representing the database. Defaults to None.
            token_data (str, optional): The token_data of the user to retrieve. Defaults to None.
                If a dictionary is passed as token_data, it should contain user data.

        Returns:
            UserInDB: A UserInDB object if the user is found, otherwise None.

        Raises:
            ValueError: If the input is invalid.

        Examples:
            db = {
                "tim": {
                    "username": "tim",
                    "full_name": "Tim Ruscica",
                    "email": "tim@gmail.com",
                    "idm_role": "idm2bcd_VCPathfinder_Viewer_BluePrint",
                    "hashed_password": "$2b$12$HxWHkvMuL7WrZad6lcCfluNFj1/Zp63lvP5aUrKlSTYtoFzPXHOtu",
                    "disabled": False,
                    }
                }
            # Example using a database dictionary:
            user = AuthenticationMiddleware.get_user(db={"tim": {...}}, username="tim")

            # Example using a user dictionary:
            user = AuthenticationMiddleware.get_user(username={"username": "tim", ...})
        """
        if db is not None and isinstance(token_data, str):
            # TODO: customize this feature to use a real database
            if token_data in db:
                token_data = db[token_data]
                return UserInDB(**token_data)
            else:
                return None  # User not found in the database

        elif isinstance(token_data, dict):
            token_data = token_data
            return UserInDB(**token_data)
        else:
            raise ValueError(
                "Invalid input: Either 'db' and 'token_data' (str) or 'token_data' (dict) must be provided."
            )


def generate_access_token():
    form_data = DATABASE["tim"]
    form_data = OAuth2PasswordRequestForm(
        username=form_data["username"], password="tim1234"
    )
    token_generator = GenAccToken()
    token_data = token_generator.login_for_access_token(form_data=form_data)[
        "access_token"
    ]
    msg.text(token_data, color="green")

    current_user = token_generator.get_current_user(token=token_data)
    msg.info(f"Current User\n {current_user}")
    return token_data
