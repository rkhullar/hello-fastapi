from mongoengine import Document
from mongoengine.fields import StringField, BooleanField
from typing import Optional


class User(Document):
    username: str = StringField(required=True)
    email: Optional[str] = StringField()
    full_name: Optional[str] = StringField()
    disabled: Optional[bool] = BooleanField()
    hashed_password: str = StringField(required=True)
    salt: str = StringField(required=True)
