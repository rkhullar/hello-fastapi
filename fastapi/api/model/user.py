from typing import List, Optional

from mongoengine import Document
from mongoengine.fields import BooleanField, ListField, StringField

from ..core.util import document_extras


@document_extras
class User(Document):
    username: str = StringField(required=True, unique=True)
    email: Optional[str] = StringField(required=True, unique=True)
    full_name: Optional[str] = StringField(required=True)
    disabled: Optional[bool] = BooleanField()
    scopes: List[str] = ListField(StringField())
    hashed_password: str = StringField(required=True)
    salt: str = StringField(required=True)

    meta = {
        'indexes': ['username']
    }

    def add_scope(self, scope: str):
        self.update(add_to_set__scopes=scope)

    def del_scope(self, scope: str):
        self.update(pull__scopes=scope)
