from fastapi import APIRouter, Depends
from sqlmodel import select
from google.genai import types

from .prompts import DOCS
from .models.user import User
from .authService import Payload, get_payload
from .models.history import History, HistoryCreate
from .db import SessionDep
from .gemini import client

history_router = APIRouter(prefix="/history")

FEEDBACK_PROMPT = """
Ты тренер по подготовке полицейских. 
Твоя задача помочь пользователю проанализировать переговоры. 
Выдай фидбэк в формате:
{
    "analysis": "<анализ>",
    "cons": ["недостаток"],
    "pros": ["достойнство"],
}
Вот материалы для переговоров:
""" + DOCS

@history_router.get("/feedback/{id}")
async def get_docs(id: int, session: SessionDep):
    msg = session.exec(select(History).where(History.id == id)).first().messages
    return client.models.generate_content(model="gemini-2.0-flash", 
                                          contents=msg,
                                          config=types.GenerateContentConfig(
            system_instruction=FEEDBACK_PROMPT,
            response_mime_type="application/json"
        )).text

@history_router.get("/me")
async def get_me(session: SessionDep, payload: Payload = Depends(get_payload)):
    user = session.exec(select(User).where(User.id == payload.id)).first()
    history = []
    for i in user.get_history():
        history.append(session.exec(select(History).where(History.id == i)).first())
    return history


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
