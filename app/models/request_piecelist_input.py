from pydantic import BaseModel
from typing import Literal

class RequestPieceListInput(BaseModel):
    context: Literal["chess", "shogi"]
    theme: Literal["green", "classicwood", "set1", "set2"]
