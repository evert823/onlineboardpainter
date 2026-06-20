from app.classes.piecelist_provider import PieceListProvider
import config
import os

def piecedefinitions_loc():
    s = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv")
    return s


def chushogipiecedefinitions_loc():
    s = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "chushogipiecedefinitions.csv")
    return s


plprov = PieceListProvider(piecedefinitions_loc=piecedefinitions_loc())
plprov.load_piece_definitions()
#dict2 = plprov.provide_piecelist_context_chess(theme="green")
dict2 = plprov.provide_piecelist_context_chess(theme="classicwood")

#plprov = PieceListProvider(piecedefinitions_loc=chushogipiecedefinitions_loc())
#plprov.load_piece_definitions()
#dict2 = plprov.provide_piecelist_context_shogi(theme="set1")
#dict2 = plprov.provide_piecelist_context_shogi(theme="set2")

print(dict2)
