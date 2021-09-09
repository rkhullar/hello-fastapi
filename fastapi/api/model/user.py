from typing import List, Optional

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

    def verify_password(self, plain_password: str) -> bool:
        return HashFactory().hash_data(password=plain_password, salt=self.salt) == self.hashed_password

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['User']:
        user = cls.get(username=username)
        if user and user.verify_password(plain_password=password):
            return user
