import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types

from .prompts import DOCS
from .config import Settings

client = genai.Client(api_key=Settings().GOOGLE_GEMINI_KEY)

gemini_router = APIRouter(prefix="/negotiations")

@gemini_router.websocket("/ws")
async def negotiation(websocket: WebSocket):
    await websocket.accept()
    try:
        chat = client.chats.create(model="gemini-2.0-flash", config=types.GenerateContentConfig(
            system_instruction="Ты тренер по подготовке полицейских. Твоя задача помочь пользователю по вопросам прав. Не форматируй ответ. Так же используй сайт Вот материалы для переговоров: \n" + DOCS
        ))
        while True:
            data = await websocket.receive_text()
            for i, chunk in enumerate(chat.send_message_stream(data)):
                await websocket.send_text(json.dumps({ "idx": i, "chunk": chunk.text }))
    except WebSocketDisconnect:
        pass