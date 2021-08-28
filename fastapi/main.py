from factory import create_app
import uvicorn
import os

environment = os.getenv('ENVIRONMENT', 'tbd')
debug = bool(os.getenv('DEBUG', 0))
app = create_app(environment=environment)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=debug)
