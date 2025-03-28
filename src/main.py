from typing import Union

from fastapi.staticfiles import StaticFiles
from .users import user_router
from .files import file_router
from fastapi import FastAPI
from . import db


app = FastAPI(on_startup=[db.create_db_and_tables])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(file_router)
app.include_router(user_router)