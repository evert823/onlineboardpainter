from app.models.boardpainter_input import BoardPainterInput
from datetime import datetime
import os
from app.classes.board_painter import BoardPainter
from app.classes.fen_handler import FENHandler

def process_text(input: BoardPainterInput):
    # Your logic here

    fenh = FENHandler(piecedefinitions_loc="/home/administrator/chess_variant_boardpainter/piecedefinitions/piecedefinitions.csv")
    fenh.load_piece_definitions()

    myjsontext = input.text
    a = fenh.detect_JSON(inputtext=input.text)
    if a == False:
        try:
            rc, myjsontext = fenh.convert_fen_to_JSON(input.text)
            assert rc == 0
        except Exception as e:
            return {"message": f"Trying to detect either FEN or JSON but neither worked. error: {e}"}

    file_name = tempfilename()
    output_dir = "/home/administrator/onlineboardpainter/useroutput"
    file_path = os.path.join(output_dir, "json", f"{file_name}.json")
    file2 = open(file_path, "w",  encoding="utf-8")
    file2.write(myjsontext)
    file2.close()

    try:
        create_board(file_name=file_name, output_dir=output_dir, theme=input.theme)
        return {
            "message": f"User input stored as {file_name}.json.",
            "image_file": f"{file_name}.png"
        }

    except Exception as e:
        return {"message": f"Creating {file_name}.png did not go entirely as we had in mind. Error: {e}"}

def create_board(file_name, output_dir, theme):
    myboardpainter = BoardPainter()
    file_path = os.path.join(output_dir, "json", f"{file_name}.json")
    image_path = os.path.join(output_dir, "boardimages", f"{file_name}.png")

    if theme == "classicwood":
        myboardpainter.pieceimages_folder = "pieceimages_classicwood"
        myboardpainter.pieceimages_extension = "png"
        myboardpainter.a1_is_white = False

    myboardpainter.load_file(file_path)
    myboardpainter.create_board_image_and_save(image_path)

def tempfilename():
    myfilename_datetimepart = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    myfilename = "usr_pos_" + myfilename_datetimepart
    return myfilename

