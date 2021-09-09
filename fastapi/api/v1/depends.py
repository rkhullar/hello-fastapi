from dataclasses import dataclass
from typing import Tuple

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from ..core.config import Settings
from ..core.util import TokenData, TokenFactory
from ..model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='./api/v1/login')


async def get_token_factory(request: Request) -> TokenFactory:
    settings: Settings = request.app.extra['settings']
    return TokenFactory(secret_key=settings.secret_key)


async def get_token_data(token: str = Depends(oauth2_scheme), token_factory: TokenFactory = Depends(get_token_factory)) -> TokenData:
    return await token_factory.parse(token)


async def get_current_user(token: str = Depends(oauth2_scheme), token_factory: TokenFactory = Depends(get_token_factory)) -> User:
    to_raise = HTTPException(status_code=401, detail='could not validate token')
    token_data = await token_factory.parse(token)
    if token_data:
        identity = token_data.sub
        _type, name = identity.split(':')
        if _type != 'username':
            raise to_raise
        user = User.get(username=name)
        if not user:
            raise to_raise
        return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='inactive user')
    return current_user


@dataclass(frozen=True)
class AllowedScopes:
    scopes: Tuple[str]

    def __call__(self, token_data: TokenData = Depends(get_token_data)):
        # TODO: verify logic
        if not set(self.scopes).intersection(token_data.scopes):
            raise HTTPException(status_code=403, detail='forbidden')


def allowed_scopes(*scopes: str):
    def decorator(fn):
        dependency = Depends(AllowedScopes(scopes))
        fn.api_route.dependencies.append(dependency)
        return fn
    return decorator
