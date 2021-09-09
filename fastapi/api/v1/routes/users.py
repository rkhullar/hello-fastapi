from typing import List

from ...core.router import APIRouter
from ...model import User as UserInDB
from ..depends import allowed_scopes
from ..schema import User

router = APIRouter()


@allowed_scopes('admin')
@router.get('/', response_model=List[User])
async def list_users():
    return list(UserInDB.objects.all())
