from pydantic import BaseModel
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from api.middlewares.gen_access_token import GenAccToken

router = APIRouter()

class GenToken(BaseModel):
    access_token: str
    token_type: str

@router.post("/login_for_access_token", response_model=GenToken, tags=["Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_info = OAuth2PasswordRequestForm(
        username=form_data.username, password=form_data
    )
    token_data = GenAccToken().generate(form_data=user_info)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data