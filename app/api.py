from fastapi import APIRouter
from app.models.text_input import TextInput
from app.services.makeboard import process_text
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/onlineboardpainter/api/makeboard")
def hello():
    return {"message": "Hello from FastAPI!"}

@router.post("/onlineboardpainter/api/makeboard")
def receive_text(input: TextInput):
    return process_text(input)

@router.get("/onlineboardpainter/api/image/{image_file}")
def get_image(image_file: str):
    output_dir = "/home/administrator/onlineboardpainter/useroutput/boardimages"
    file_path = os.path.join(output_dir, image_file)
    return FileResponse(path=file_path, media_type='image/png')
