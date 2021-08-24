from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from jose import jwt
import datetime as dt
import os
from util.hash import build_json_hash

SECRET_KEY = os.environ['SECRET_KEY']
SESSION_DURATION = 30  # minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='./api/v1/login')

router = APIRouter()


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
    salt: str


fake_users_db = {
    'person': UserInDB(username='person', full_name='Person Test', email='noreply@example.com', hashed_password='vALXtyEJwIc8BK4Rqm8pi7NXJ6WWlitZdD78JanTOQkK7UPcRpEJL3YQt6PL7nXDtcxGg2NqkEP7DgVF7L5ACQ==', salt='bFIP5irOtSG7Jreu')
}


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    return build_json_hash(data={'password': plain_password}, salt=salt) == hashed_password


def authenticate_user(db: dict, username: str, password: str) -> Optional[UserInDB]:
    if username in db:
        user = db[username]
        if verify_password(plain_password=password, hashed_password=user.hashed_password, salt=user.salt):
            return user


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
    user = authenticate_user(fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401)
    access_token = create_access_token(data={'sub': f'username:{user.username}'},
                                       duration=dt.timedelta(minutes=SESSION_DURATION))
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me')
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
