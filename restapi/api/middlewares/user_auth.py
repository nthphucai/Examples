import sys
import os
from typing import Optional, Union

from fastapi import Depends, Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from fastapi.security import APIKeyHeader

sys.path.append("backend/VCP_athfinder/app")

from .gen_access_token import GenAccToken

class TokenData(BaseModel):
    username: str
    idm_role: str
    hashed_password: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    idm_role: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str

oauth2_scheme = APIKeyHeader(name="API-Key", auto_error=False)


# Middleware to handle user authentication
class AuthenticationMiddleware(BaseHTTPMiddleware):
    ALGORITHM = "HS256"

    token_generator = GenAccToken()

    async def dispatch(self, request: Request, call_next):
        """
        Middleware method to handle user authentication by verifying the presence
        and validity of an authentication token in the request headers.
        Args:
            request (Request): The incoming HTTP request object.
            call_next (Callable): The next middleware or endpoint to be called.
        Returns:
            JSONResponse: A response with a 401 status code if the authentication
            token is missing or invalid.
            Response: The response from the next middleware or endpoint if the
            authentication token is valid.
        """
        if request.method in ["OPTIONS", "GET"]:
            return await call_next(request)
        
        # Skip authentication for the login_for_access_token endpoint
        if request.url.path == "/login_for_access_token":
            return await call_next(request)
        
        # Perform authentication for other endpoints
        bearer_data = request.headers.get("Authorization")
        token = bearer_data.replace("Bearer ", "") if bearer_data else None

        if not token:
            return JSONResponse(
                content="Missing authentication token.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not self._verify_token(token):
            return JSONResponse(
                content="Invalid authentication token.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return await call_next(request)

    def _verify_token(self, token: str = Depends(oauth2_scheme)) -> bool:
        """
        Verifies the provided authentication token and checks if the current user has the Viewer role.
        Args:
            token (str): The authentication token to be verified.
        Returns:
            bool: True if the token is valid and the current user has the Viewer role, False otherwise.
        Raises:
            HTTPException: If the authentication token is invalid, an HTTP 401 Unauthorized response is returned.
        """
        try:
            current_user = self.token_generator.get_current_user(token)
            print(f"Current_user: {current_user}")
            return current_user.idm_role == "Viewer"

        except HTTPException:
            JSONResponse(
                content="Invalid authentication token.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
