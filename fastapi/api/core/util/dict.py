import functools


def dict_args(fn):
    @functools.wraps(fn)
    def wrapper(data: dict = None, /, *args, **extra):
        params = dict()
        params.update(data or dict())
        params.update(extra)
        return fn(params)
    return wrapper


@dict_args
def parse_dict_args(data: dict) -> dict:
    return data


if __name__ == '__main__':

    @dict_args
    def hello(data: dict):
        return data

    assert hello(data=7, extra=7) == dict(data=7, extra=7)
    assert hello({'a': 1, 'b': 2}, c=3, d=4) == dict(a=1, b=2, c=3, d=4)

    # TODO: try to get decorator to work for methods
    # class Fact:
    #     @dict_args
    #     def world(self, data: dict):
    #         return data
    #
    # fact = Fact()
    # assert fact.world(data=7, extra=7) == dict(data=7, extra=7)
    # assert fact.world({'a': 1, 'b': 2}, c=3, d=4) == dict(a=1, b=2, c=3, d=4)
