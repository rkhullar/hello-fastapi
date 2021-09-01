from mongoengine.errors import DoesNotExist


def _build_extra(kls):
    class DocumentExtras:

        @classmethod
        def get(cls, raise_error: bool = False, **query):
            try:
                return kls.objects.get(**query)
            except DoesNotExist as err:
                if raise_error:
                    raise err

        def dict(self):
            return self.to_mongo().to_dict()

    return DocumentExtras


def document_extras(cls):
    to_inject = _build_extra(cls)
    for member in ['get', 'dict']:
        setattr(cls, member, getattr(to_inject, member))
    return cls
