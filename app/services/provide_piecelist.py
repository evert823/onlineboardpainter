from app.models.request_piecelist_input import RequestPieceListInput
from app.classes.piecelist_provider import PieceListProvider

def process_request_for_piecelist(input: RequestPieceListInput):
    if input.context == "chess":
        try:
            plprov = PieceListProvider(piecedefinitions_loc="/home/administrator/onlineboardpainter/resources/piecedefinitions/piecedefinitions.csv")
            plprov.load_piece_definitions()
            dict2 = plprov.provide_piecelist_context_chess(theme=input.theme)
        except Exception as e:
            return {"message": f"Provide piecelist context chess failed. error: {e}"}
    else:
        try:
            plprov = PieceListProvider(piecedefinitions_loc="/home/administrator/onlineboardpainter/resources/piecedefinitions/chushogipiecedefinitions.csv")
            plprov.load_piece_definitions()
            dict2 = plprov.provide_piecelist_context_shogi(theme=input.theme)
        except Exception as e:
            return {"message": f"Provide piecelist context shogi failed. error: {e}"}
    return {
        "message": f"Provide piecelist succeeded.",
        "piecelist_dict": dict2
    }
