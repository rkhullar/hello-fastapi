from fastapi import APIRouter, Security
from typing import List

from ...model import User as UserInDB
from ..schema import User
from ..depends import get_current_active_user

router = APIRouter()


@router.get('/', response_model=List[User])
async def list_users(current_user: User = Security(get_current_active_user, scopes=['hello'])):
    return [UserInDB.get(username='groundx14')]
