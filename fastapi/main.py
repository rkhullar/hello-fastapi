from factory import create_app
import uvicorn
from config import Settings

settings = Settings()
app = create_app(settings)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.service_host, port=settings.service_port, reload=settings.debug)
