import os
import config
from app.models.fen_json_converter_input import FENJsonConverterInput
from app.classes.fen_handler import FENHandler

def process_fen_json(input: FENJsonConverterInput):
    if input.context == "chess":
        fenh = FENHandler(piecedefinitions_loc=os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv"))
    else:
        fenh = FENHandler(piecedefinitions_loc=os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "chushogipiecedefinitions.csv"))
    fenh.load_piece_definitions()

    if input.direction == "fen2json":
        try:
            rc, myjsontext = fenh.convert_fen_to_JSON(fentext=input.text)
            assert rc == 0
        except Exception as e:
            return {"message": f"Convert FEN to JSON failed. error: {e}"}
        return {
            "message": f"Convert FEN to JSON succeeded.",
            "converted_text": f"{myjsontext}"
        }
    else:
        fenh.pieceID_separation_strategy = input.pieceID_separation_strategy
        try:
            myfentext = fenh.convert_JSON_to_fen(jsontext=input.text)
        except Exception as e:
            return {"message": f"Convert JSON to FEN failed. error: {e}"}
        return {
            "message": f"Convert JSON to FEN succeeded.",
            "converted_text": f"{myfentext}"
        }
