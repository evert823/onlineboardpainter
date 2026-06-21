from app.models.fen_json_converter_input import FENJsonConverterInput
from app.classes.format_dispatcher import FormatDispatcher

def process_fen_json(input: FENJsonConverterInput):
    MyFormatDispatcher = FormatDispatcher()

    try:
        myoutputtext = MyFormatDispatcher.convert_format(inputtext=input.text,
                                                         pieceID_separation_strategy=input.pieceID_separation_strategy,
                                                         context=input.context)
    except Exception as e:
        return {"message": f"Convert failed. error: {e}"}
    return {
        "message": f"Convert succeeded.",
        "converted_text": f"{myoutputtext}"
    }
