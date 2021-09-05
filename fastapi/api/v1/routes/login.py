from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ...core.util import TokenFactory
from ...model import User as UserInDB
from ..depends import get_current_active_user, get_token_factory
from ..schema import Token, User

router = APIRouter()


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), token_factory: TokenFactory = Depends(get_token_factory)):
    user = UserInDB.authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='incorrect username or password')
    access_token = await token_factory.build(sub=f'username:{user.username}')
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user
