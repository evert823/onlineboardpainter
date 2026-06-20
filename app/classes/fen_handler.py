from app.classes.chess_position import ChessPosition
from app.classes.piece_name_handler import PieceNameHandler
import config
import os
import json

class FENHandler:
    def __init__(self, piecedefinitions_loc=os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv")):
        self.MyChessPosition = ChessPosition()
        self.MyPieceNameHandler = PieceNameHandler()
        self.piecedefinitions_loc = piecedefinitions_loc
        self.fen_pieceplacements = ""
        self.fen_activecolor = ""
        self.fen_castling_av = ""
        self.fen_eptargetsquare = ""
        self.fen_halfmoveclock = ""
        self.fen_fullmovenumber = ""
        self.special_nonalf = ["'", '`', '"', '~', '^', '!', ':']
        #self.pieceID_separation_strategy = "comma"
        self.pieceID_separation_strategy = "squarebracket"

    def load_piece_definitions(self):
        self.MyPieceNameHandler.load_piece_definitions(filename=self.piecedefinitions_loc)
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("K")
        assert symbol_found == True and mytest == "King"
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol(".")
        assert symbol_found == True and mytest == ""

    def convert_JSON_to_fen(self, jsontext):
        self.MyChessPosition.load_from_jsontext(jsontext=jsontext)
        problematic_pieceIDs_found = self.has_problematic_pieceIDs()
        fenparts = []
        for j in range(self.MyChessPosition.boardheight):
            rj = (self.MyChessPosition.boardheight - 1) - j
            vacantcount = 0
            fenpart = ""
            for i in range(self.MyChessPosition.boardwidth):
                if self.MyChessPosition.squares[rj][i] != '.':
                    if vacantcount != 0:
                        fenpart += str(vacantcount)
                        if problematic_pieceIDs_found == True and self.pieceID_separation_strategy == "comma":
                            fenpart += ","
                        vacantcount = 0
                    mysymbol = self.pieceID_for_fen(self.MyChessPosition.squares[rj][i])
                    if problematic_pieceIDs_found == True and self.pieceID_separation_strategy == "squarebracket":
                        fenpart += f"[{mysymbol}]"
                    else:
                        fenpart += mysymbol
                    if problematic_pieceIDs_found == True and self.pieceID_separation_strategy == "comma":
                        fenpart += ","
                if self.MyChessPosition.squares[rj][i] == '.':
                    vacantcount += 1
            if vacantcount != 0:
                fenpart += str(vacantcount)
                if problematic_pieceIDs_found == True and self.pieceID_separation_strategy == "comma":
                    fenpart += ","
            if fenpart.endswith(","):
                fenpart = fenpart[:-1]
            fenparts.append(fenpart)
        fen = "/".join(fenparts)
        if self.MyChessPosition.colourtomove == 1:
           fen += " w"
        else:
           fen += " b"
        return fen


    def has_problematic_pieceIDs(self):
        for j in range(self.MyChessPosition.boardheight):
            for i in range(self.MyChessPosition.boardwidth):
                mysymbol = self.MyChessPosition.squares[j][i]
                if mysymbol.startswith('-'):
                     mysymbol = mysymbol[1:]

                if len(mysymbol) == 1:
                    pass
                elif (mysymbol[0].isalpha() == True and mysymbol[1] in self.special_nonalf
                           and len(mysymbol) < 3):
                    pass
                else:
                    return True
        return False

    def pieceID_for_fen(self, symbol):
        if symbol.startswith('-'):
            return symbol[1:].lower()
        else:
            return symbol.upper()

    def convert_fen_to_JSON(self, fentext):
        try:
            self.decompose_fen_1(fentext=fentext)
        except Exception as e:
            return 1, str(e)

        try:
            self.handle_pieceplacements()
        except Exception as e:
            return 1, str(e)

        try:
            myjson = self.create_JSON()
        except Exception as e:
            return 1, str(e)

        return 0, myjson

    def decompose_fen_1(self, fentext):
        #Get the 6 fields from the full fentext
        #We tolerate FENs containing less than 6 fields or even 1 field
        fenparts = fentext.split(" ")
        self.fen_pieceplacements = fenparts[0]
        if self.fen_pieceplacements == "":
            raise Exception("No valid FEN")
        if self.fen_pieceplacements[0].isalnum() == False and self.fen_pieceplacements[0] not in ['[']:
            raise Exception(f"FEN starting with {self.fen_pieceplacements[:5]} no valid FEN")

        try:
            self.fen_activecolor = fenparts[1]
        except:
            self.fen_activecolor = ""

        try:
            self.fen_castling_av = fenparts[2]
        except:
            self.fen_castling_av = ""

        try:
            self.fen_eptargetsquare = fenparts[3]
        except:
            self.fen_eptargetsquare = ""

        try:
            self.fen_halfmoveclock = fenparts[4]
        except:
            self.fen_halfmoveclock = ""

        try:
            self.fen_fullmovenumber = fenparts[5]
        except:
            self.fen_fullmovenumber = ""

    def handle_pieceplacements(self):
        fenranks = self.fen_pieceplacements.split("/")
        maxw = -1
        a3 = []
        for a1 in fenranks:
            a2 = self.parse_one_rank(a1)
            a3.append(a2)
            if len(a2) > maxw:
                maxw = len(a2)
        self.MyChessPosition.reset_boardsize(maxw, len(fenranks))
        for j in range(self.MyChessPosition.boardheight):
            rj = (self.MyChessPosition.boardheight - 1) - j
            for i in range(self.MyChessPosition.boardwidth):
                try:
                    self.MyChessPosition.squares[rj][i] = self.handle_pieceID(onesquare=a3[j][i])
                except:
                    self.MyChessPosition.squares[rj][i] = '.'

    def handle_pieceID(self, onesquare):
        s = "."
        for item in self.MyPieceNameHandler.piecedict["piecedefinitions"]:
            if item["piecesymbol"].upper() == onesquare.upper():
                if onesquare == onesquare.lower():
                    s = "-" + item["piecesymbol"]
                elif onesquare == onesquare.upper():
                    s = item["piecesymbol"]
        return s

    def parse_one_rank(self, fenrank):
        if fenrank.find("[") > -1:
            pieces = self.parse_one_rank_if_square_brackets(fenrank=fenrank)
        elif fenrank.find(",") > -1:
            pieces = self.parse_one_rank_if_comma_separated(fenrank=fenrank)
        else:
            pieces = self.parse_one_rank_if_no_separator(fenrank=fenrank)
        return pieces

    def parse_one_rank_if_no_separator(self, fenrank):
        pieces = []
        i = 0
        n = len(fenrank)
        while i < n:
            c = fenrank[i]
            # Handle empty squares
            if c.isdigit():
                num = c
                i += 1
                while i < n and fenrank[i].isdigit():
                    num += fenrank[i]
                    i += 1
                pieces.extend([''] * int(num))
                continue
            # Handle letter + special nonalf as one piece
            if c.isalpha() and i + 1 < n and fenrank[i+1] in self.special_nonalf:
                pieces.append(c + fenrank[i+1])
                i += 2
                continue
            # Handle normal single-char piece
            pieces.append(c)
            i += 1
        return pieces

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

    def parse_one_rank_if_square_brackets(self, fenrank):
        pieces = []

        i = 0
        n = len(fenrank)
        while i < n:
            c = fenrank[i]
            # Handle empty squares
            if c.isdigit():
                num = c
                i += 1
                while i < n and fenrank[i].isdigit():
                    num += fenrank[i]
                    i += 1
                pieces.extend([''] * int(num))
                continue
            # Handle one piece between square brackets
            if c == "[":
                i += 1
                mysymbol = ""
                while i < n and fenrank[i] != "]":
                    mysymbol += fenrank[i]
                    i += 1
                pieces.append(mysymbol)
            else:
                raise Exception(f"Incomplete square brackets detected")
            i += 1
        return pieces

    def create_JSON(self):
        minlen = self.MyChessPosition.max_len_symbol()
        if minlen < 3:
            minlen = 3

        positiondict = {}
        positiondict["boardwidth"] = self.MyChessPosition.boardwidth
        positiondict["boardheight"] = self.MyChessPosition.boardheight
        if self.fen_activecolor == "w":
            positiondict["colourtomove"] = 1
        else:
            positiondict["colourtomove"] = -1
        
        #For now we don't write fen_castling_av, fen_eptargetsquare,
        #fen_halfmoveclock or fen_fullmovenumber to the JSON

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

    def detect_JSON(self, inputtext):
        try:
            mydict = json.loads(inputtext)
        except:
            return False
        if "boardwidth" in mydict:
            return True
        return False
