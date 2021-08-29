from typing import NamedTuple


def _make_extra(kls):
    class Extra:
        def hello(self):
            print('hello world')

        def world(self):
            print(self.name, self.age)

        @classmethod
        def test_cls(cls):
            print(kls.test_base())
    return Extra


def make_extra(cls):
    kls = _make_extra(cls)
    for member in ['hello', 'world', 'test_cls']:
        print('setting', cls.__name__, member)
        setattr(cls, member, getattr(kls, member))
    return cls


@make_extra
class Person(NamedTuple):
    name: str
    age: int = 0

    @classmethod
    def test_base(cls):
        return 'test base'

    def test_link(self):
        self.test_cls()


if __name__ == '__main__':
    p = Person(name='person')
    p.test_link()
