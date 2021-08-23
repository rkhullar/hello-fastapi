from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from jose import jwt
import datetime as dt
import os

SECRET_KEY = os.environ['SECRET_KEY']
SESSION_DURATION = 30  # minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='./api/v1/login')

router = APIRouter()


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decode_token(token: str) -> User:
    return User(username=f'test-{token}', email='noreply@example.com', full_name='Test User')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


def create_access_token(data: dict, duration: dt.timedelta, expiration_key: str = 'exp') -> str:
    expiration = dt.datetime.utcnow() + duration
    to_encode = dict(data, **{expiration_key: expiration})
    return jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm='HS256')


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(username=form_data.username)
    access_token = create_access_token(data={'sub': f'username:{user.username}'},
                                       duration=dt.timedelta(minutes=SESSION_DURATION))
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me')
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
