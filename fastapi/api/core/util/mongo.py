from mongoengine import Document
from mongoengine.errors import DoesNotExist
from pymongo.collection import Collection


def _build_extra(kls):
    class DocumentExtras:

        @classmethod
        def get(cls, raise_error: bool = False, **query) -> Document:
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

    return DocumentExtras


def document_extras(cls):
    to_inject = _build_extra(cls)
    for member in ['get', 'dict', 'collection']:
        setattr(cls, member, getattr(to_inject, member))
    return cls
