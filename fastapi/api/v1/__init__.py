from fastapi import APIRouter

from . import items, login, users

router = APIRouter()
router.include_router(login.router, tags=['login'])
router.include_router(users.router, prefix='/users', tags=['users'])
router.include_router(users.router, prefix='/items', tags=['items'])
