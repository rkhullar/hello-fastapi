from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: Optional[bool] = None
    scopes: Optional[List[str]] = None

    class Config:
        orm_mode = True
