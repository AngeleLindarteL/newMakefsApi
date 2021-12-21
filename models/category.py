from typing import List
from pydantic import BaseModel

class Category(BaseModel):
    region: str
    tags: list