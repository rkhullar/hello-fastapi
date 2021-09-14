from nose.tools import assert_equal

from ...model import User
from .base import FastApiTest, MongoTest


class UserTest(MongoTest):

    def test_empty(self):
        assert_equal(len(User.objects.all()), 0)


class HelloTest(FastApiTest):

    def test_canary(self):
        response = self.client.get('/api/v1/me')
        assert_equal(response.status_code, 401)
