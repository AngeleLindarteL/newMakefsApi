from pydantic import BaseModel

class VRecipe(BaseModel):
    recipeid: int
    viewedSeconds: int
    videoDuration: int