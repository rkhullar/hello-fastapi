from dataclasses import dataclass

import requests
from nose.tools import assert_equal, nottest

from ...model import User
from .base import FastApiTest, MongoTest


@nottest
def create_test_user(username: str = 'test', plain_password: str = 'password') -> User:
    hashed_password, salt = User.build_password_and_salt(plain_password=plain_password)
    user = User(username=username, email='noreply@example.com', full_name='Test User',
                hashed_password=hashed_password, salt=salt)
    return user.save()


class UserTest(MongoTest):

    def test_empty(self):
        assert_equal(len(User.objects.all()), 0)


@dataclass
class BearerAuth(requests.auth.AuthBase):
    token: str

    def __call__(self, request):
        request.headers['authorization'] = f'Bearer {self.token}'
        return request


class HelloTest(FastApiTest):

    def test_auth(self):
        create_test_user(username='test', plain_password='password')
        response = self.client.post('/api/v1/login', data=dict(username='test', password='password'))
        assert_equal(response.status_code, 200)
        token = response.json()['access_token']
        response = self.client.get('/api/v1/me', auth=BearerAuth(token))
        assert_equal(response.status_code, 200)
