from unittest import TestCase

import mongoengine

from fastapi.testclient import TestClient

from ...core.config import Settings
from ...core.factory import create_app


class MongoTest(TestCase):
    load: bool = False

    @classmethod
    def setUpClass(cls):
        mongoengine.connect(name='test', alias='default', host='mongomock://localhost')
        cls.mongo_client = mongoengine.get_connection(alias='default')
        if cls.load:
            cls.load_hook()

    @classmethod
    def tearDownClass(cls):
        mongoengine.disconnect()

    @classmethod
    def load_hook(cls):
        # TODO: placeholder for loading sample data
        pass


class FastApiTest(MongoTest):

    @staticmethod
    def build_settings() -> Settings:
        return Settings(environment='test', debug=True, secret_key='secret',
                        mongo_host='', mongo_username='', mongo_password='')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings = cls.build_settings()
        app = create_app(settings, test=True)
        cls.client = TestClient(app)
        cls.settings = settings
