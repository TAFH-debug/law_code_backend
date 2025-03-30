import json
from sqlmodel import Field, SQLModel
from datetime import datetime

class HistoryBase(SQLModel):
    name: str = Field(index=True)
    score: int = Field(index=True)
    messages: str = Field(default="")

class History(HistoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())

class HistoryCreate(HistoryBase):
    pass