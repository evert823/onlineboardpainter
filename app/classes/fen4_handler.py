from app.classes.chess_position import ChessPosition
from app.classes.piece_name_handler import PieceNameHandler
from app.classes.fen_handler import FENHandler
import config
import os
import json

class FEN4Handler:
    def __init__(self, piecedefinitions_loc=os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv")):
        self.MyChessPosition = ChessPosition()
        self.MyPieceNameHandler = PieceNameHandler()
        self.piecedefinitions_loc = piecedefinitions_loc
        self.pieceID_separation_strategy = "comma" #FEN4 is actually always comma

    def load_piece_definitions(self):
        self.MyPieceNameHandler.load_piece_definitions(filename=self.piecedefinitions_loc)
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("K")
        assert symbol_found == True and mytest == "King"
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol(".")
        assert symbol_found == True and mytest == ""

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
            if a[0] in ['b', 'g', 'r', 'y', 'be', 'gn', 'rd', 'yw']:
                s = a[0][0] + a[1].upper()
            elif a[0] in ['bk']:
                s = a[1].lower()
            else:
                s = a[1].upper()
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
        
        fenranks = [s.replace("/", "") for s in fenparts[1:] if len(s) > 0]
        self.handle_pieceplacements(fenranks=fenranks)

        try:
            myjson = self.create_JSON()
        except Exception as e:
            return 1, str(e)

        return 0, myjson

    def handle_pieceplacements(self, fenranks):
        maxw = -1
        a3 = []
        for a1 in fenranks:
            #FEN4 is always comma-separated
            a2 = self.parse_one_rank_if_comma_separated(a1)
            a3.append(a2)
            if len(a2) > maxw:
                maxw = len(a2)
        self.MyChessPosition.reset_boardsize(maxw, len(fenranks))
        for j in range(self.MyChessPosition.boardheight):
            rj = (self.MyChessPosition.boardheight - 1) - j
            for i in range(self.MyChessPosition.boardwidth):
                try:
                    self.MyChessPosition.squares[rj][i] = self.parse_one_piece_from_FEN4(fenpiece=a3[j][i])
                except:
                    self.MyChessPosition.squares[rj][i] = '.'

    def parse_one_rank_if_comma_separated(self, fenrank):
        pieces = []
        a = fenrank.split(",")
        for item in a:
            try:
                addemptysquares = int(item)
                pieces.extend([''] * addemptysquares)
            except:
                pieces.append(item.strip())
        return pieces

    def parse_one_piece_from_FEN4(self, fenpiece):
        if len(fenpiece) > 1:
            if fenpiece[0] in ["r", "b", "y", "g"]:
                colorpart = fenpiece[0]
                piecepart = fenpiece[1:]
            else:
                colorpart = ''
                piecepart = fenpiece
        else:
            colorpart = ''
            piecepart = fenpiece

        confirmedpiecepart = "."
        for item in self.MyPieceNameHandler.piecedict["piecedefinitions"]:
            if item["piecesymbol"].upper() == piecepart.upper():
                confirmedpiecepart = item["piecesymbol"]
        
        if colorpart == '':
            if piecepart == confirmedpiecepart.lower():
                return '-' + confirmedpiecepart
            return confirmedpiecepart

        return colorpart + '.' + confirmedpiecepart


    def create_JSON(self):
        minlen = self.MyChessPosition.max_len_symbol()
        if minlen < 3:
            minlen = 3

        positiondict = {}
        positiondict["boardwidth"] = self.MyChessPosition.boardwidth
        positiondict["boardheight"] = self.MyChessPosition.boardheight
        positiondict["colourtomove"] = self.MyChessPosition.colourtomove

        positiondict["squares"] = []
        for j in range(self.MyChessPosition.boardheight):
            rj = (self.MyChessPosition.boardheight - 1) - j
            myvisualrank = ""
            for i in range(self.MyChessPosition.boardwidth):
                mysymbol = self.MyChessPosition.squares[rj][i]
                while len(mysymbol) < minlen:
                    mysymbol = " " + mysymbol
                myvisualrank += mysymbol
                if i < self.MyChessPosition.boardwidth - 1:
                    myvisualrank += "|"
            positiondict["squares"].append(myvisualrank)

        return json.dumps(positiondict, indent=4)
