from app.classes.chess_position import ChessPosition
from app.classes.piece_name_handler import PieceNameHandler
from app.classes.fen_handler import FENHandler
import json

class FEN4Handler:
    def __init__(self, piecedefinitions_loc="/home/administrator/onlineboardpainter/resources/piecedefinitions/piecedefinitions.csv"):
        self.MyChessPosition = ChessPosition()
        self.MyPieceNameHandler = PieceNameHandler()
        self.piecedefinitions_loc = piecedefinitions_loc
        self.pieceID_separation_strategy = "comma" #FEN4 is actually always comma

    def load_piece_definitions(self):
        self.MyPieceNameHandler.load_piece_definitions(filename=self.piecedefinitions_loc)
        mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("K")
        assert mytest == "King"
        mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol(".")
        assert mytest == ""

    def convert_JSON_to_fen(self, jsontext):
        self.MyChessPosition.load_from_jsontext(jsontext=jsontext)
        fenparts = []
        for j in range(self.MyChessPosition.boardheight):
            rj = (self.MyChessPosition.boardheight - 1) - j
            vacantcount = 0
            fenpart = ""
            for i in range(self.MyChessPosition.boardwidth):
                if self.MyChessPosition.squares[rj][i] != '.':
                    if vacantcount != 0:
                        fenpart += str(vacantcount)
                        fenpart += ","
                        vacantcount = 0
                    mysymbol = self.pieceID_for_fen(self.MyChessPosition.squares[rj][i])
                    fenpart += mysymbol
                    fenpart += ","
                if self.MyChessPosition.squares[rj][i] == '.':
                    vacantcount += 1
            if vacantcount != 0:
                fenpart += str(vacantcount)
                fenpart += ","
            if fenpart.endswith(","):
                fenpart = fenpart[:-1]
            fenparts.append(fenpart)
        fen = "\n".join(fenparts)

        line0 = ""
        if self.MyChessPosition.colourtomove == 1:
           line0 += "W"
        elif self.MyChessPosition.colourtomove == 11:
           line0 += "R"
        elif self.MyChessPosition.colourtomove == 12:
           line0 += "B"
        elif self.MyChessPosition.colourtomove == 13:
           line0 += "Y"
        elif self.MyChessPosition.colourtomove == 14:
           line0 += "G"
        else:
           line0 += "B"
        line0 += "-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-"
        fen = line0 + "\n" + fen

        return fen

    def pieceID_for_fen(self, symbol):
        if symbol.startswith('-'):
            return symbol[1:].lower()
        elif symbol.find('.') == -1:
            return symbol.upper()
        else:
            a = symbol.split('.')
            if a[0] == 'yw':
                s = 'y'
            elif a[0] == 'gn':
                s = 'g'
            elif a[0] == 'rd':
                s = 'r'
            elif a[0] == 'be':
                s = 'b'
            else:
                s = a[0].lower()
            s += a[1].upper()
            return s

    def convert_fen_to_JSON(self, fentext):
        fenparts = fentext.split("\n")
        fenactivecolour = fenparts[0][0]
        if fenactivecolour == "W":
            self.MyChessPosition.colourtomove = 1
        elif fenactivecolour == "R":
            self.MyChessPosition.colourtomove = 11
        elif fenactivecolour == "B":
            self.MyChessPosition.colourtomove = 12
        elif fenactivecolour == "Y":
            self.MyChessPosition.colourtomove = 13
        elif fenactivecolour == "G":
            self.MyChessPosition.colourtomove = 14
        else:
            self.MyChessPosition.colourtomove = -1
        
        try:
            myjson = self.create_JSON()
        except Exception as e:
            return 1, str(e)

        return 0, myjson

    def create_JSON(self):
        positiondict = {}
        positiondict["boardwidth"] = self.MyChessPosition.boardwidth
        positiondict["boardheight"] = self.MyChessPosition.boardheight
        return json.dumps(positiondict, indent=4)
