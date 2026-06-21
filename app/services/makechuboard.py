from app.models.chuboardpainter_input import ChuBoardPainterInput
from datetime import datetime
import config
import os
from app.classes.format_dispatcher import FormatDispatcher

def process_text4chu(input: ChuBoardPainterInput):
    MyFormatDistpatcher = FormatDispatcher()
    file_name = tempfilename()
    jsonfilepath = os.path.join(config.USEROUTPUT_ROOT, "json", f"{file_name}.json")
    imagefilepath = os.path.join(config.USEROUTPUT_ROOT, "boardimages", f"{file_name}.png")

    try:
        MyFormatDistpatcher.make_board(inputtext=input.text,
                                       context="shogi",
                                       theme=input.theme,
                                       jsonfilepath=jsonfilepath,
                                       imagefilepath=imagefilepath)
        return {
            "message": f"User input stored as {file_name}.json.",
            "image_file": f"{file_name}.png"
        }

    except Exception as e:
        return {"message": f"Creating {file_name}.png did not go entirely as we had in mind. Error: {e}"}

def tempfilename():
    myfilename_datetimepart = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    myfilename = "usr_pos_" + myfilename_datetimepart
    return myfilename
