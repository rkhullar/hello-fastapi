import mongoengine

from fastapi import FastAPI

from ..router import router as api_router
from .config import Settings


def link_mongo(settings: Settings):
    for name in settings.mongo_db_names:
        mongoengine.connect(db=name, alias=name, host=settings.mongo_uri, connect=False)


def create_app(settings: Settings, test: bool = False) -> FastAPI:
    app = FastAPI(settings=settings)
    app.include_router(api_router, prefix='/api')
    if not test:
        link_mongo(settings)
    return app
