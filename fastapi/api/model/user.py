from typing import List, Optional, Tuple

from mongoengine import Document
from mongoengine.fields import BooleanField, ListField, StringField

from ..core.util import HashFactory, document_extras


@document_extras
class User(Document):
    username: str = StringField(required=True, unique=True)
    email: Optional[str] = StringField(required=True, unique=True)
    full_name: Optional[str] = StringField(required=True)
    disabled: Optional[bool] = BooleanField()
    roles: List[str] = ListField(StringField())
    hashed_password: str = StringField(required=True)
    salt: str = StringField(required=True)

    meta = {
        'indexes': ['username']
    }

    def add_role(self, role: str):
        self.update(add_to_set__roles=role)

    def del_role(self, role: str):
        self.update(pull__roles=role)

    @staticmethod
    def build_password_and_salt(plain_password: str) -> Tuple[str, str]:
        hash_factory = HashFactory()
        salt = hash_factory.build_salt()
        hashed_password = hash_factory.hash_data(password=plain_password, salt=salt)
        return hashed_password, salt

    def update_password(self, plain_password: str):
        hashed_password, salt = self.build_password_and_salt(plain_password)
        return self.update(set__hashed_password=hashed_password, set__salt=salt)

    def verify_password(self, plain_password: str) -> bool:
        return HashFactory().hash_data(password=plain_password, salt=self.salt) == self.hashed_password

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['User']:
        user = cls.get(username=username)
        if user and user.verify_password(plain_password=password):
            return user

    @classmethod
    def create_with_password(cls, plain_password: str, **kwargs) -> 'User':
        hashed_password, salt = cls.build_password_and_salt(plain_password=plain_password)
        kwargs.update(dict(hashed_password=hashed_password, salt=salt))
        return cls.create(**kwargs)
