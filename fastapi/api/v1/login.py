import os
from typing import Optional

from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..config import Settings
from ..model import User as UserInDB
from ..util.hash import build_json_hash
from ..util.jwt import TokenFactory

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='./api/v1/login')


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


async def get_token_factory(settings: Settings = Depends()) -> TokenFactory:
    return TokenFactory(secret_key=settings.secret_key)


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    return build_json_hash(data={'password': plain_password}, salt=salt) == hashed_password


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = UserInDB.get(username=username)
    if user and verify_password(plain_password=password, hashed_password=user.hashed_password, salt=user.salt):
        return user


async def get_current_user(token: str = Depends(oauth2_scheme), token_factory: TokenFactory = Depends(get_token_factory)) -> UserInDB:
    to_raise = HTTPException(status_code=401, detail='could not validate token')
    token_data = await token_factory.parse(token)
    if token_data:
        identity = token_data.sub
        _type, name = identity.split(':')
        if _type != 'username':
            raise to_raise
        user = UserInDB.get(username=name)
        if not user:
            raise to_raise
        return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='inactive user')
    return current_user


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), token_factory: TokenFactory = Depends(get_token_factory)):
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='incorrect username or password')
    access_token = await token_factory.build(data={'sub': f'username:{user.username}'})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user
