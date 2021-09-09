from typing import List

from fastapi import Depends, HTTPException

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
        # TODO: verify logic
        if not set(self.scopes).intersection(token_data.scopes):
            raise HTTPException(status_code=403, detail='forbidden')


def allowed_scopes(*scopes: str):
    def decorator(fn):
        dependency = Depends(AllowedScopes(*scopes))
        fn.api_route.dependencies.append(dependency)
        return fn
    return decorator


@router.get('/1', response_model=List[User], dependencies=[Depends(AllowedScopes('admin'))])
async def list_users_1():
    return list(UserInDB.objects.all())


@allowed_scopes('admin')
@router.get('/2', response_model=List[User])
async def list_users_2():
    return list(UserInDB.objects.all())
