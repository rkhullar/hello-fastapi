from typing import Callable, List, Optional

from fastapi import Depends, HTTPException
from fastapi.routing import APIRoute

from ...core.router import APIRouter
from ...core.util import TokenData
from ...model import User as UserInDB
from ..depends import get_token_data
from ..schema import User

router = APIRouter()


class AllowedScopes:

    def __init__(self, *scopes: str):
        self.scopes = scopes

    def __call__(self, token_data: TokenData = Depends(get_token_data)):
        # print(self.scopes)
        # print(token_data)
        if not set(self.scopes).intersection(token_data.scopes):
            raise HTTPException(status_code=403, detail='forbidden')


def find_route_for(router: APIRouter, fn: Callable) -> Optional[APIRoute]:
    for route in router.routes:
        if route.endpoint == fn:
            return route


def allowed_scopes(router: APIRouter, *scopes: str):
    def decorator(fn):
        route = find_route_for(router, fn)
        route.dependencies.append(Depends(AllowedScopes(*scopes)))
        return fn
    return decorator


@router.get('/', response_model=List[User], dependencies=[Depends(AllowedScopes('admin'))])
async def list_users_1():
    return [UserInDB.get(username='groundx14')]


@allowed_scopes(router, 'admin')
@router.get('/2', response_model=List[User])
async def list_users_2():
    return [UserInDB.get(username='groundx14')]
