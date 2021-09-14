from unittest import TestCase
from nose.tools import assert_equal
import mongoengine
from ...model import User


class HelloTest(TestCase):

    def test_hello(self):
        assert_equal(1, 1)


class MongoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        mongoengine.connect(name='test', alias='default', host='mongomock://localhost')
        cls.mongo_client = mongoengine.get_connection(alias='default')

    @classmethod
    def tearDownClass(cls):
        mongoengine.disconnect()

    def test_user(self):
        assert_equal(len(User.objects.all()), 0)
