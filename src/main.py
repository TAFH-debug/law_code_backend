from fastapi.staticfiles import StaticFiles
from .users import user_router
from .files import file_router
from .resources import resource_router
from .gemini import gemini_router
from .simulations import simulations_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from . import db

app = FastAPI(on_startup=[db.create_db_and_tables])
app.include_router(file_router)
app.include_router(user_router)
app.include_router(resource_router)
app.include_router(gemini_router)
app.include_router(simulations_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}