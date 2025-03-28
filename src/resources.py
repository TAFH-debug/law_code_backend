from fastapi import APIRouter
from sqlmodel import select

from .models import *
from .db import SessionDep


resource_router = APIRouter(prefix="/resources")

@resource_router.get("/")
async def get_resources(session: SessionDep):
    return session.exec(select(Resource)).all()


@resource_router.get("/{resource_id}")
async def get_resource(resource_id: int, session: SessionDep):
    return session.exec(select(Resource).where(Resource.id == resource_id)).first()

@resource_router.post("/")
async def create_resource(resource: ResourceCreate, session: SessionDep):
    db_resource = Resource.model_validate(resource)
    session.add(db_resource)
    session.commit()
    return resource