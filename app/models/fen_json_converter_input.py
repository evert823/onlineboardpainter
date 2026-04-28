from pydantic import BaseModel
from typing import Literal

class FENJsonConverterInput(BaseModel):
    text: str
    direction: Literal["fen2json", "json2fen"]
    context: Literal["chess", "shogi"]
    pieceID_separation_strategy: Literal["comma", "squarebracket"]
