from pydantic import BaseModel
from typing import Literal

class ChuBoardPainterInput(BaseModel):
    text: str
    theme: Literal["set1", "set2"]
