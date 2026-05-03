from fastapi import APIRouter
from app.models.boardpainter_input import BoardPainterInput
from app.models.chuboardpainter_input import ChuBoardPainterInput
from app.models.text_input import TextInput
from app.services.makeboard import process_text
from app.services.makechuboard import process_text4chu
from app.services.authenticate import verify_test_text
from fastapi.responses import FileResponse
from app.models.fen_json_converter_input import FENJsonConverterInput
from app.services.convertfenjson import process_fen_json
from app.models.request_piecelist_input import RequestPieceListInput
from app.services.provide_piecelist import process_request_for_piecelist
import os

router = APIRouter()

@router.get("/onlineboardpainter/api/makeboard")
def hello():
    return {"message": "Hello from FastAPI!"}

@router.post("/onlineboardpainter/api/makeboard")
def receive_text(input: BoardPainterInput):
    return process_text(input)

@router.get("/onlineboardpainter/api/makechuboard")
def hello():
    return {"message": "Hello from FastAPI!"}

@router.post("/onlineboardpainter/api/makechuboard")
def receive_text(input: ChuBoardPainterInput):
    return process_text4chu(input)

@router.post("/onlineboardpainter/api/authenticate")
def receive_text(input: TextInput):
    return verify_test_text(input)

@router.get("/onlineboardpainter/api/image/{image_file}")
def get_image(image_file: str):
    output_dir = "/home/administrator/onlineboardpainter/useroutput/boardimages"
    file_path = os.path.join(output_dir, image_file)
    return FileResponse(path=file_path, media_type='image/png')

@router.get("/onlineboardpainter/api/pieceimage")
def get_pieceimage(image_file_path: str):
    return FileResponse(path=image_file_path, media_type='image/png')

@router.post("/onlineboardpainter/api/convertfenjson")
def convert_fenjson(input: FENJsonConverterInput):
    return process_fen_json(input)

@router.post("/onlineboardpainter/api/providepiecelist")
def provide_piecelist(input: RequestPieceListInput):
    return process_request_for_piecelist(input)
