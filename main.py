from enum import Enum
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'hello world'}


@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    messages = {
        ModelName.alexnet: 'Deep Learning FTW!',
        ModelName.resnet: 'Have some residuals',
        ModelName.lenet: 'LeCNN all the images'
    }
    return {'model': model_name, 'message': messages[model_name]}


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


fake_items_db = [
    {'item_name': 'Foo'},
    {'item_name': 'Bar'},
    {'item_name': 'Baz'}
]


@app.get('/items')
async def read_item(skip: int = 0, limit: int = 0):
    return fake_items_db[skip:skip+limit]


@app.get('/items/{item_id}')
async def read_item(item_id: int, q: Optional[str] = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update(q=q)
    if not short:
        item.update(description='This is an amazing item that has a long description')
    return item


@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(user_id: int, item_id: int, needy: str, skip: int = 0, limit: Optional[int] = None):
    return dict(user_id=user_id, item_id=item_id, needy=needy, skip=skip, limit=limit)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post('/items')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        item_dict['price_with_tax'] = item.price + item.tax
    return item_dict


@app.post('/items/{item_id')
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    item_dict = {'item_id': item_id, **item.dict()}
    if q:
        item_dict['q'] = q
    return item_dict
