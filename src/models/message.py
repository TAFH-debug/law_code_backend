from sqlmodel import SQLModel


class Message(SQLModel):
    author: str
    content: str