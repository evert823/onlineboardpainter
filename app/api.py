from fastapi import APIRouter
from app.models.text_input import TextInput
from app.services.makeboard import process_text

router = APIRouter()

@router.get("/onlineboardpainter/api/makeboard")
def hello():
    return {"message": "Hello from FastAPI!"}

@router.post("/onlineboardpainter/api/makeboard")
def receive_text(input: TextInput):
    return process_text(input)
