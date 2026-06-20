class PieceNameHandler:
    def __init__(self):
        self.piecedict = {"piecedefinitions" : []}

    def load_piece_definitions(self, filename="/home/administrator/onlineboardpainter/resources/piecedefinitions/piecedefinitions.csv"):
        File1 = open(filename, 'r')
        Lines = File1.readlines()
        File1.close()
        self.piecedict = {"piecedefinitions" : []}
        for line in Lines:
            if line[:21] != "piecesymbol,piecename":
                a = line.replace("\n", "").split(",")
                mydict = {"piecesymbol" : a[0], "piecename" : a[1]}
                self.piecedict["piecedefinitions"].append(mydict)

    def lookup_piecename_by_symbol(self, psymbol: str) -> str:
        """
        Returns tuple symbol_found, piecename
        symbol_found False indicates an issue with non-trivial input that was not defined
        dot and whitespace indicate a vacant square
        """
        for item in self.piecedict["piecedefinitions"]:
            if item["piecesymbol"] == psymbol:
                return True, item["piecename"]
        if psymbol.strip() == "":
            return True, ""
        if psymbol.strip() == ".":
            return True, ""
        return False, ""
