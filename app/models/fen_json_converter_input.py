from pydantic import BaseModel
from typing import Literal

class FENJsonConverterInput(BaseModel):
    text: str
    context: Literal["chess", "shogi"]
    pieceID_separation_strategy: Literal["comma", "squarebracket"]
