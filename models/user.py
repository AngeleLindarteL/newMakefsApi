from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    _id: Optional[str]
    uid: int
    categories: dict
    chefs: list
    rnv: list
    vw: dict