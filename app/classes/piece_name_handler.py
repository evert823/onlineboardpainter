class PieceNameHandler:
    def __init__(self):
        self.piecedict = {"piecedefinitions" : []}

    def load_piece_definitions(self, filename="/home/administrator/chess_variant_boardpainter/piecedefinitions/piecedefinitions.csv"):
        File1 = open(filename, 'r')
        Lines = File1.readlines()
        for line in Lines:
            if line[:21] != "piecesymbol,piecename":
                a = line.replace("\n", "").split(",")
                mydict = {"piecesymbol" : a[0], "piecename" : a[1]}
                self.piecedict["piecedefinitions"].append(mydict)

    def lookup_piecename_by_symbol(self, psymbol: str) -> str:
        for item in self.piecedict["piecedefinitions"]:
            if item["piecesymbol"] == psymbol:
                return item["piecename"]
        return ""
