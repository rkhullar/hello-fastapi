from fastapi import APIRouter
from ..model import User


router = APIRouter()


@router.get('/test')
async def test_user():
    print(User.objects())
    return {'message': 'hello world'}


'''
@router.get('/first-user')
async def first_user():
    user = User(
        username='person',
        full_name='Person Test',
        email='noreply@example.com',
        hashed_password='REDACTED',
        salt='REDACTED'
    )
    user.save()
    return dict()
'''
