from sqlmodel import SQLModel


class ResourceBase(SQLModel):
    href: str
    name: str
    description: str

class ResourceCreate(ResourceBase):
    pass
