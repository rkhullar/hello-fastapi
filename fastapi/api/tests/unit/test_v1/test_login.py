from nose.tools import assert_dict_contains_subset, assert_equal, nottest

from ....core.util import BearerAuth
from ....model import User
from ..base import FastApiTest


@nottest
def create_test_user(username: str = 'test', plain_password: str = 'password') -> User:
    return User.create_with_password(username=username, plain_password=plain_password,
                                     email='noreply@example.com', full_name='Test User')


class LoginTest(FastApiTest):

    def test_self_with_auth(self):
        create_test_user(username='test', plain_password='password')
        response = self.client.post('/api/v1/login', data=dict(username='test', password='password'))
        assert_equal(response.status_code, 200)
        token = response.json()['access_token']
        response = self.client.get('/api/v1/me', auth=BearerAuth(token))
        assert_equal(response.status_code, 200)
        assert_dict_contains_subset({'username': 'test'}, response.json())

    def test_self_no_auth(self):
        response = self.client.get('/api/v1/me')
        assert_equal(response.status_code, 401)
