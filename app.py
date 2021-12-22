from fastapi import FastAPI
from routes.routes import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI()

origins = [
    "https://makefs.site",
    "https://makefs.site/",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user)