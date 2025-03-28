from fastapi import APIRouter, Depends
from sqlmodel import select
from .db import SessionDep
from .models import *
from .authService import Payload, get_payload, jwt_service
from passlib.context import CryptContext


user_router = APIRouter(prefix="/users")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@user_router.get("/")
def get_all_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

@user_router.get("/secured")
def secured(session: SessionDep, payload: Payload = Depends(get_payload)):
    user = session.exec(select(User).where(User.id == payload.id)).first()
    return user

@user_router.post("/")
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate({
        "username": user.username,
        "hashed_password": pwd_context.hash(user.password)
    })
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@user_router.post("/login")
def login_user(user: UserLogin, session: SessionDep):
    user_id = session.exec(select(User.id).where(User.username == user.username)).first()
    token = jwt_service.sign(Payload(user_id))
    return { "token": token }

@user_router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep):
    user = session.exec(select(User).where(User.id == user_id)).first()
    return user