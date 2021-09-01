from functools import lru_cache
from typing import List

import mongoengine

from fastapi import Depends, FastAPI

from . import router as api_router
from .config import Settings


def link_mongo(settings: Settings):
    for name in settings.mongo_db_names:
        mongoengine.connect(db=name, alias=name, host=settings.mongo_uri, connect=False)


def build_global_depends(settings: Settings) -> List[Depends]:
    @lru_cache
    async def read_settings() -> Settings:
        return settings
    return [Depends(read_settings)]


def create_app(settings: Settings) -> FastAPI:
    global_depends = build_global_depends(settings)
    app = FastAPI(dependencies=global_depends)
    app.include_router(api_router, prefix='/api')
    link_mongo(settings)
    return app
