from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .gemini import client
from .prompts import SIMULATION_PROMPT
from google.genai import types

simulations_router = APIRouter(prefix="/simulations")

MISSION = """
{
    "hostages": [
    {
        "имя": "Айгуль",
        "возраст": 35,
        "пол": "женский",
        "национальность": "казашка",
        "медицинская_информация": {
        "группа_крови": "A+",
        "аллергии": ["пыльца"]
        },
        "дополнительная_информация": "Учительница, замужем, двое детей."
    },
    {
        "имя": "Борис",
        "возраст": 42,
        "пол": "мужской",
        "национальность": "русский",
        "медицинская_информация": {
        "группа_крови": "O-",
        "аллергии": []
        },
        "дополнительная_информация": "Инженер, увлекается шахматами."
    },
    {
        "имя": "Чингиз",
        "возраст": 28,
        "пол": "мужской",
        "национальность": "уйгур",
        "медицинская_информация": {
        "группа_крови": "B+",
        "аллергии": ["лактоза"]
        },
        "дополнительная_информация": "Студент, занимается спортом."
    }]
}
"""

@simulations_router.websocket("/ws")
async def start_simulation(websocket: WebSocket, id: int):
    await websocket.accept()
    try:
        chat = client.chats.create(model="gemini-2.0-flash", config=types.GenerateContentConfig(
            system_instruction=SIMULATION_PROMPT,
            response_mime_type="application/json"
        ))
        message = chat.send_message(MISSION)
        await websocket.send_text(message.text)

        while True:
            text = await websocket.receive_text()
            message = chat.send_message(text)
            await websocket.send_text(message.text)
    except WebSocketDisconnect:
        pass