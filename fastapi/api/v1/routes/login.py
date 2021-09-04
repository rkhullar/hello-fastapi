from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ...core.util import HashFactory, TokenFactory
from ...model import User as UserInDB
from ..depends import get_current_active_user, get_token_factory
from ..schema import Token, User

router = APIRouter()


async def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    return HashFactory().hash_data(password=plain_password, salt=salt) == hashed_password


async def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = UserInDB.get(username=username)
    if user and await verify_password(plain_password=password, hashed_password=user.hashed_password, salt=user.salt):
        return user


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), token_factory: TokenFactory = Depends(get_token_factory)):
    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='incorrect username or password')
    access_token = await token_factory.build(data={'sub': f'username:{user.username}'})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user
