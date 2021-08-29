import mongoengine

from api import router as api_router
from config import Settings
from fastapi import FastAPI


def link_mongo(settings: Settings):
    for name in settings.mongo_db_names:
        mongoengine.connect(db=name, alias=name, host=settings.mongo_uri, connect=False)


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix='/api')
    link_mongo(settings)
    return app
