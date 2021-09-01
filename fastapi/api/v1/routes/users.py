from fastapi import APIRouter

from ...model import User as UserInDB
from ..schema import User

router = APIRouter()


@router.get('/test', response_model=User)
async def test_user():
    return UserInDB.get(username='person')
