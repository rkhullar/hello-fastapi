from fastapi import APIRouter as DefaultRouter


class APIRouter(DefaultRouter):
    def api_route(self, *args, **kwargs):
        parent_decorator = super().api_route(*args, **kwargs)

        def decorator(fn):
            parent_decorator(fn)
            fn.api_route = self.routes[-1]
            assert fn.__qualname__ == fn.api_route.endpoint.__qualname__
            return fn

        return decorator
