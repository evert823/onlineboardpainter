from app.classes.piece_name_handler import PieceNameHandler
import os

class PieceListProvider:
    def __init__(self, piecedefinitions_loc="/home/administrator/onlineboardpainter/resources/piecedefinitions/piecedefinitions.csv"):
        self.MyPieceNameHandler = PieceNameHandler()
        self.piecedefinitions_loc = piecedefinitions_loc
        self.resourcespath = "/home/administrator/onlineboardpainter/resources/"

    def load_piece_definitions(self):
        self.MyPieceNameHandler.load_piece_definitions(filename=self.piecedefinitions_loc)
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("K")
        assert symbol_found == True and mytest == "King"
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol(".")
        assert symbol_found == True and mytest == ""

    def provide_piecelist_context_chess(self, theme="green"):
        dict2 = {"piecedefinitions": []}
        for item in self.MyPieceNameHandler.piecedict["piecedefinitions"]:
            item2 = {"piecesymbol": item["piecesymbol"], "piecename":item["piecename"]}
            item2["imagefilepath"] = self.get_imagefilename_context_chess(piecename=item["piecename"], theme=theme)
            dict2["piecedefinitions"].append(item2)
        return dict2

    def get_imagefilename_context_chess(self, piecename, theme="green"):
        if theme == "green":
            path = self.resourcespath + "pieceimages/"
            extension = "jpg"
        else:
            path = self.resourcespath + "pieceimages_classicwood/"
            extension = "png"
        myfilename = f"white{piecename.lower()}onwhite.{extension}"
        if os.path.exists(f"{path}{myfilename}") == True:
            return f"{path}{myfilename}"
        else:
            myfilename = f"_notfoundonwhite.{extension}"
            return f"{path}{myfilename}"

    def provide_piecelist_context_shogi(self, theme="set1"):
        dict2 = {"piecedefinitions": []}
        for item in self.MyPieceNameHandler.piecedict["piecedefinitions"]:
            item2 = {"piecesymbol": item["piecesymbol"], "piecename":item["piecename"]}
            item2["imagefilepath"] = self.get_imagefilename_context_shogi(piecename=item["piecename"], theme=theme)
            dict2["piecedefinitions"].append(item2)
        return dict2

    def get_imagefilename_context_shogi(self, piecename, theme="set1"):
        if theme == "set1":
            path = self.resourcespath + "shogi_set1/"
        else:
            path = self.resourcespath + "shogi_set2/"
        extension = "png"
        myfilename = f"{piecename.lower()}_sente.{extension}"
        myfilename_promoted = f"{piecename.lower()}_sente_promoted.{extension}"
        if os.path.exists(f"{path}{myfilename}") == True:
            return f"{path}{myfilename}"
        elif os.path.exists(f"{path}{myfilename_promoted}") == True:
            return f"{path}{myfilename_promoted}"
        else:
            myfilename = f"_notfound.{extension}"
            return f"{path}{myfilename}"
