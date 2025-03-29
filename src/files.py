from fastapi import APIRouter, UploadFile
from uuid import uuid4


file_router = APIRouter(prefix="/files")

@file_router.post("/upload")
async def create_file(file: UploadFile):
    extension = file.filename.split(".")[-1]
    filename = uuid4().hex + "." + extension
    with open("./static/" + filename, "wb") as f:
        f.write(file.file.read())

    return { "filename": filename }