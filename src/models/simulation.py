from sqlmodel import Field, SQLModel


class SimulationBase(SQLModel):
    name: str = Field(index=True)
    description: str = Field(index=True)
    prompt: str = Field(index=True)

class Simulation(SimulationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class SimulationCreate(SimulationBase):
    pass
