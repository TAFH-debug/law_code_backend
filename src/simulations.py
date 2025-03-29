from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlmodel import select

from .models.simulation import Simulation, SimulationCreate
from .db import SessionDep
from .gemini import client
from .prompts import DOCS, SIMULATION_PROMPT

from google.genai import types

simulations_router = APIRouter(prefix="/simulations")


@simulations_router.post("/")
async def create_simulation(simulation: SimulationCreate, session: SessionDep):
    db_simulation = Simulation.model_validate(simulation)
    session.add(db_simulation)
    session.commit()
    session.refresh(db_simulation)
    return db_simulation

@simulations_router.get("/")
async def get_simulations(session: SessionDep):
    return session.exec(select(Simulation)).all()

@simulations_router.websocket("/ws")
async def start_simulation(websocket: WebSocket, id: int, session: SessionDep):
    await websocket.accept()
    simulation = session.exec(select(Simulation).where(Simulation.id == id)).first()
    try:
        chat = client.chats.create(model="gemini-2.0-flash", config=types.GenerateContentConfig(
            system_instruction=SIMULATION_PROMPT + DOCS,
            response_mime_type="application/json"
        ))
        message = chat.send_message(simulation.prompt)
        await websocket.send_text(message.text)

        while True:
            text = await websocket.receive_text()
            message = chat.send_message(text)
            await websocket.send_text(message.text)
    except WebSocketDisconnect:
        pass