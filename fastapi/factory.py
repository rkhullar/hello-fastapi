from fastapi import FastAPI
from api import router as api_router
from config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix='/api')
    return app
