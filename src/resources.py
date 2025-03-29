from fastapi import APIRouter
from sqlmodel import select

from .models import *
from .db import SessionDep


resource_router = APIRouter(prefix="/resources")

@resource_router.get("/")
async def get_resources(session: SessionDep, limit: int = 6, page: int = 1):
    resources = session.exec(select(Resource).limit(limit).offset((page - 1) * limit)).all()
    pages = len(session.exec(select(Resource)).all())
    return {
        "resources": resources,
        "page": page,
        "limit": limit,
        "total_pages": (pages + limit - 1) // limit,
    }

@resource_router.get("/{resource_id}")
async def get_resource(resource_id: int, session: SessionDep):
    return session.exec(select(Resource).where(Resource.id == resource_id)).first()

@resource_router.post("/")
async def create_resource(resource: ResourceCreate, session: SessionDep):
    db_resource = Resource.model_validate(resource)
    session.add(db_resource)
    session.commit()
    return resource