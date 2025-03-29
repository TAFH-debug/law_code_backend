from sqlmodel import Field, SQLModel


class ResourceBase(SQLModel):
    url: str = Field(index=True)
    name: str = Field(index=True)
    description: str = Field(index=True)
    type: str = Field(index=True)

class Resource(ResourceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
class ResourceCreate(ResourceBase):
    pass
