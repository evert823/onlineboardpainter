from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow CORS for testing (optional, but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/onlineboardpainter/api/makeboard")
def hello():
    return {"message": "Hello from FastAPI!"}

class TextInput(BaseModel):
    text: str

@app.post("/onlineboardpainter/api/makeboard")
def receive_text(input: TextInput):
    # For now, just echo the received text length
    return {"message": f"Received {len(input.text.splitlines())} lines of text."}

