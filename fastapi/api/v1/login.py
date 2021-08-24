import datetime as dt
import os
from typing import Optional

from jose import JWTError, jwt
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..util.hash import build_json_hash

SECRET_KEY = os.environ['SECRET_KEY']
SESSION_DURATION = 30  # minutes
JWT_ALGORITHM = 'HS256'

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


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    to_raise = HTTPException(status_code=401, detail='could not validate token')
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[JWT_ALGORITHM])
        identity = payload['sub']
        _type, name = identity.split(':')
        if _type != 'username':
            raise to_raise
    except JWTError:
        raise to_raise
    user = fake_users_db.get(name)
    if not user:
        raise to_raise
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='inactive user')
    return current_user


def create_access_token(data: dict, duration: dt.timedelta, expiration_key: str = 'exp') -> str:
    expiration = dt.datetime.utcnow() + duration
    to_encode = dict(data, **{expiration_key: expiration})
    return jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=JWT_ALGORITHM)


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='incorrect username or password')
    access_token = create_access_token(data={'sub': f'username:{user.username}'},
                                       duration=dt.timedelta(minutes=SESSION_DURATION))
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user
