from fastapi import FastAPI
from routes.routes import user

app = FastAPI()

app.include_router(user)