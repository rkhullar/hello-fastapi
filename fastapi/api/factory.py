from typing import List

import mongoengine

from fastapi import Depends, FastAPI, Request

from . import router as api_router
from .config import Settings


def link_mongo(settings: Settings):
    for name in settings.mongo_db_names:
        mongoengine.connect(db=name, alias=name, host=settings.mongo_uri, connect=False)


def build_global_depends() -> List[Depends]:
    def read_settings(request: Request) -> Settings:
        return request.app.extra['settings']
    return [
        Depends(read_settings)
    ]


def create_app(settings: Settings) -> FastAPI:
    global_depends = build_global_depends()
    app = FastAPI(dependencies=global_depends)
    app.extra['settings'] = settings
    app.include_router(api_router, prefix='/api')
    link_mongo(settings)

    # @app.middleware('http')
    # async def add_settings(request: Request, call_next):
    #     request.settings = settings
    #     response = await call_next(request)
    #     return response

    return app
