from fastapi import APIRouter
from sqlmodel import select
from google.genai import types

from .models.history import History, HistoryCreate
from .db import SessionDep
from .gemini import client

history_router = APIRouter(prefix="/history")

@history_router.get("/")
async def get_histories(session: SessionDep):
    histories = session.exec(select(History)).all()
    return histories

@history_router.get("/{id}")
async def get_history(id: int, session: SessionDep):
    return session.exec(select(History).where(History.id == id)).first()

@history_router.post("/")
async def create_history(history: HistoryCreate, session: SessionDep): 
    db_history = History.model_validate(history)
    session.add(db_history)
    session.commit()
    session.refresh(db_history)
    return db_history

@history_router.get("/{id}")
async def get_recommendations(id: int):
    return client.models.generate_content("gemini-2.0-flash", 
                                          contents="",
                                          config=types.GenerateContentConfig(
            system_instruction="Ты тренер по подготовке полицейских. Твоя задача помочь пользователю проанализировать переговоры. Не форматируй ответ. Вот материалы для переговоров: \n" + DOCS
        ))