from pydantic import BaseModel
from typing import Literal

class BoardPainterInput(BaseModel):
    text: str
    theme: Literal["green", "classicwood"]
