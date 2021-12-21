from pydantic import BaseModel

class Chef(BaseModel):
    chefid: int
    viewedTime: int
    rate: float
    savedRecipes: int
    isReported: bool