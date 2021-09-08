from fastapi import APIRouter
from typing import List

from ...model import User as UserInDB
from ..schema import User

router = APIRouter()


@router.get('/', response_model=List[User])
async def list_users():
    return [UserInDB.get(username='groundx14')]
