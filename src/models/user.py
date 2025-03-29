import json
from typing import List
from sqlmodel import ARRAY, Column, Field, Integer, SQLModel

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    score: int = Field(default=0)
    passed_simulation_ids: str = Field(default="[]")
    passed_cyber_simulation_ids: str = Field(default="[]")

    def get_psi(self) -> List[int]:
        return json.loads(self.passed_simulation_ids) if self.passed_simulation_ids else []

    def set_psi(self, new_values: List[int]):
        self.passed_simulation_ids = json.dumps(new_values)

    def get_pcsi(self) -> List[int]:
        return json.loads(self.passed_cyber_simulation_ids) if self.passed_cyber_simulation_ids else []
    
    def set_pcsi(self, new_values: List[int]):
        self.passed_cyber_simulation_ids = json.dumps(new_values)
    


        
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(index=True)

class UserCreate(SQLModel):
    username: str
    password: str

class UserLogin(SQLModel):
    username: str
    password: str
    