
from fastapi import APIRouter
from sqlmodel import select

from .db import SessionDep
from .models import User


user_router = APIRouter(prefix="/users")


@user_router.get("/")
def get_all_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users
