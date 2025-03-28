import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google import genai
from .config import Settings

client = genai.Client(api_key=Settings().GOOGLE_GEMINI_KEY)

gemini_router = APIRouter(prefix="/negotiations")

@gemini_router.websocket("/ws")
async def negotiation(websocket: WebSocket, id: int):
    await websocket.accept()
    try:
        chat = client.chats.create(model="gemini-2.0-flash")
        while True:
            data = await websocket.receive_text()
            for i, chunk in enumerate(chat.send_message_stream(data)):
                await websocket.send_text(json.dumps({ "idx": i, "chunk": chunk.text }))
    except WebSocketDisconnect:
        pass