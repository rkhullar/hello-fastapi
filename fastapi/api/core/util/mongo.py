from typing import Type

from mongoengine import Document
from mongoengine.errors import DoesNotExist
from pymongo.collection import Collection


def _build_extra(kls: Type[Document]):
    class DocumentExtras:

        @classmethod
        def get(cls, raise_error: bool = False, **query) -> kls:
            try:
                return kls.objects.get(**query)
            except DoesNotExist as err:
                if raise_error:
                    raise err

        def dict(self) -> dict:
            return self.to_mongo().to_dict()

        @classmethod
        def collection(cls) -> Collection:
            # TODO: try to make into class property
            return kls._get_collection()

        @classmethod
        def create(cls, *args, **kwargs) -> kls:
            doc = kls(*args, **kwargs)
            doc.save()
            return doc

    return DocumentExtras


def document_extras(cls: Type[Document]):
    to_inject = _build_extra(cls)
    for member in ['get', 'dict', 'collection', 'create']:
        setattr(cls, member, getattr(to_inject, member))
    return cls
