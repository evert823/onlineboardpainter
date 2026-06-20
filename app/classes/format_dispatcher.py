from app.classes.chess_position import ChessPosition
from app.classes.board_painter import BoardPainter
from app.classes.chu_board_painter import ChuBoardPainter
from app.classes.fen_handler import FENHandler
from app.classes.fen4_handler import FEN4Handler
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
            for j in range(self.boardheight):
                for i in range(self.boardwidth):
                    mysymbol = self.squares[j][i].strip()
                    if mysymbol != "." and mysymbol.find(".") > -1:
                        return True, True
            return True, False
        except:
            return False, False

    def classify_input(self, inputtext: str):
        is_json, is_json4 = self._classify_json(inputtext=inputtext)
        if is_json == True and is_json4 == False:
            return "JSON"
        if is_json == True and is_json4 == True:
            return "JSON4"
        if inputtext[1] == "-" and inputtext.find("\n") > -1:
            return "FEN4"
        return "FEN"





