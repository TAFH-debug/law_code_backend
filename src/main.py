from typing import Union
from .user import user_router
from fastapi import FastAPI
from . import db



def on_startup():
    db.create_db_and_tables()

app = FastAPI(on_startup=[on_startup])


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_router)