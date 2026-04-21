from app.models.chuboardpainter_input import ChuBoardPainterInput
from datetime import datetime
import os
from app.classes.chu_board_painter import ChuBoardPainter

def process_text4chu(input: ChuBoardPainterInput):
    # Your logic here
    file_name = tempfilename()
    output_dir = "/home/administrator/onlineboardpainter/useroutput"
    file_path = os.path.join(output_dir, "json", f"{file_name}.json")
    file2 = open(file_path, "w",  encoding="utf-8")
    file2.write(input.text)
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
    myboardpainter = ChuBoardPainter()
    file_path = os.path.join(output_dir, "json", f"{file_name}.json")
    image_path = os.path.join(output_dir, "boardimages", f"{file_name}.png")

    if theme == "set2":
        myboardpainter.pieceimages_folder = "/home/administrator/chu_shogi_piece_images/output_set2"

    myboardpainter.load_file(file_path)
    myboardpainter.create_board_image_and_save(image_path)

def tempfilename():
    myfilename_datetimepart = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    myfilename = "usr_pos_" + myfilename_datetimepart
    return myfilename

