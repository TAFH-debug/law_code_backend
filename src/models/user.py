from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(index=True)

class UserCreate(SQLModel):
    username: str
    password: str

class UserLogin(SQLModel):
    username: str
    password: str
    