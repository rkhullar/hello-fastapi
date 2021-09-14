import os
from typing import List, Optional

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    project: str = os.getenv('PROJECT', 'hello-fastapi')
    environment: Optional[str] = os.getenv('ENVIRONMENT')
    debug = bool(os.getenv('DEBUG', 0))


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', '0.0.0.0')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class SecuritySettings(BaseSettings):
    secret_key: str = os.getenv('SECRET_KEY')


class MongoSettings(BaseSettings):
    mongo_db_names: List[str] = ['default']
    mongo_host: str = os.getenv('MONGO_HOST')
    mongo_username: str = os.getenv('MONGO_USERNAME')
    mongo_password: str = os.getenv('MONGO_PASSWORD')
    mongo_scheme: str = 'mongodb+srv'

    @property
    def mongo_uri(self) -> str:
        base_url = f'{self.mongo_scheme}://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}'
        return f'{base_url}/default?retryWrites=true&w=majority'


class Settings(ProjectSettings, NetworkSettings, SecuritySettings, MongoSettings):
    pass
