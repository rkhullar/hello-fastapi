from fastapi import FastAPI
from api import router as api_router


def create_app(environment: str) -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix='/api')
    return app
