from app.classes.chess_position import ChessPosition
from app.classes.board_painter import BoardPainter
from app.classes.chu_board_painter import ChuBoardPainter
from app.classes.fen_handler import FENHandler
from app.classes.fen4_handler import FEN4Handler
import config
import os
import json

'''
This class helps with requests where we we want to be dynamic w.r.t. input format
Capabilities of this class:
1. Classify input as one of the following
    - FEN
    - FEN4
    - JSON
    - JSON containing a 4-player position

2. Accept conversion request between FEN and JSON and dispatch to the correct class and method

3. Accept make board request and dispatch to the correct class and method

4. Pass parameters as is, without knowledge
    - context shogi or chess
    - theme
    - pieceID separation strategy

NO validation happens against combinations that have not been implemented downstream, such as:
- 4-player combined with theme classic wood
- 4-player combined with context shogi

'''

class FormatDispatcher:
    def __init__(self):
        self.MyChessPosition = ChessPosition()
        self.MyBoardPainter = BoardPainter()
        self.MyChuBoardPainter = ChuBoardPainter()
        self.MyFENHandler = FENHandler()
        self.MyFEN4Handler = FEN4Handler()

    def _classify_json(self, inputtext: str):
        try:
            mydict = json.loads(inputtext)
        except:
            return False, False

        try:
            self.MyChessPosition.load_from_dict(positiondict=mydict)
            for j in range(self.MyChessPosition.boardheight):
                for i in range(self.MyChessPosition.boardwidth):
                    mysymbol = self.MyChessPosition.squares[j][i].strip()
                    if mysymbol != "." and mysymbol.find(".") > -1:
                        return True, True
            return True, False
        except:
            return False, False

    def prepare_piecedefinitions(self, context):
        if context == "chess":
            self.MyFENHandler.piecedefinitions_loc = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv")
            self.MyFEN4Handler.piecedefinitions_loc = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv")
        else:
            self.MyFENHandler.piecedefinitions_loc = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "chushogipiecedefinitions.csv")
            self.MyFEN4Handler.piecedefinitions_loc = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "chushogipiecedefinitions.csv")
        self.MyFENHandler.load_piece_definitions()
        self.MyFEN4Handler.load_piece_definitions()

    def make_board(self, inputtext: str, context: str, theme: str,
                   jsonfilepath: str, imagefilepath: str):
        self.prepare_piecedefinitions(context=context)
        inputformat = self.classify_input(inputtext=inputtext)
        if inputformat == "JSON":
            myjson = inputtext
        if inputformat == "JSON4":
            myjson = inputtext
        if inputformat == "FEN":
            a = self.MyFENHandler.convert_fen_to_JSON(fentext=inputtext)
            assert a[0] == 0
            myjson = a[1]
        if inputformat == "FEN4":
            a = self.MyFEN4Handler.convert_fen_to_JSON(fentext=inputtext)
            assert a[0] == 0
            myjson = a[1]

        file2 = open(jsonfilepath, "w",  encoding="utf-8")
        file2.write(myjson)
        file2.close()

        if context == "chess":
            if theme == "classicwood":
                self.MyBoardPainter.pieceimages_folder = "pieceimages_classicwood"
                self.MyBoardPainter.pieceimages_extension = "png"
                self.MyBoardPainter.a1_is_white = False
            elif theme == "green":
                self.MyBoardPainter.pieceimages_folder = "pieceimages"
                self.MyBoardPainter.pieceimages_extension = "jpg"
                self.MyBoardPainter.a1_is_white = True
            self.MyBoardPainter.load_file(jsonfilepath)
            self.MyBoardPainter.create_board_image_and_save(imagefilepath)
        elif context == "shogi":
            if theme == "set1":
                self.MyChuBoardPainter.pieceimages_folder = os.path.join(config.RESOURCES_ROOT, "shogi_set1")
            elif theme == "set2":
                self.MyChuBoardPainter.pieceimages_folder = os.path.join(config.RESOURCES_ROOT, "shogi_set2")
            self.MyChuBoardPainter.load_file(jsonfilepath)
            self.MyChuBoardPainter.create_board_image_and_save(imagefilepath)

    def convert_format(self, inputtext: str, context: str, pieceID_separation_strategy: str):
        self.prepare_piecedefinitions(context=context)
        self.MyFENHandler.pieceID_separation_strategy = pieceID_separation_strategy
        self.MyFEN4Handler.pieceID_separation_strategy = pieceID_separation_strategy
        inputformat = self.classify_input(inputtext=inputtext)
        if inputformat == "JSON":
            myfen = self.MyFENHandler.convert_JSON_to_fen(jsontext=inputtext)
            return myfen
        if inputformat == "JSON4":
            myfen = self.MyFEN4Handler.convert_JSON_to_fen(jsontext=inputtext)
            return myfen
        if inputformat == "FEN":
            myjson = self.MyFENHandler.convert_fen_to_JSON(fentext=inputtext)
            return myjson
        if inputformat == "FEN4":
            myjson = self.MyFEN4Handler.convert_fen_to_JSON(fentext=inputtext)
            return myjson

    def classify_input(self, inputtext: str):
        is_json, is_json4 = self._classify_json(inputtext=inputtext)
        if is_json == True and is_json4 == False:
            return "JSON"
        if is_json == True and is_json4 == True:
            return "JSON4"
        if inputtext[1] == "-" and inputtext.find("\n") > -1:
            return "FEN4"
        return "FEN"
