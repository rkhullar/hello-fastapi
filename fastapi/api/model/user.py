from typing import Optional

from mongoengine import Document
from mongoengine.fields import BooleanField, StringField

from ..core.util import document_extras


@document_extras
class User(Document):
    username: str = StringField(required=True, unique=True)
    email: Optional[str] = StringField()
    full_name: Optional[str] = StringField()
    disabled: Optional[bool] = BooleanField()
    hashed_password: str = StringField(required=True)
    salt: str = StringField(required=True)

    meta = {
        'indexes': ['username']
    }
