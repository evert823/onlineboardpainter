from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from app.classes.chess_position import ChessPosition
from app.classes.piece_name_handler import PieceNameHandler

class ChuBoardPainter:
    """
    Here we implement a board painter tool for
    - Chu Shogi
    - Shogi variants in general
    """
    def __init__(self):
        self.MyChessPosition = ChessPosition()
        self.MyPieceNameHandler = PieceNameHandler()
        self.pieceimages_folder = "/home/administrator/chu_shogi_piece_images/output_set1"
        self.pieceimages_extension = "png"

        #TODO make dynamic, get from json
        self.piecewidth = 180 #73
        self.pieceheight = 196 #79
        self.edgesize_top = 62 #25
        self.edgesize_bottom = 7 #3
        self.edgesize_left = 7 #3
        self.edgesize_right = 59 #24

        #self.boardcolor = (243, 226, 171)
        self.boardcolor = (204, 85, 34)
        self.boardimage = Image.new('RGB', (self.piecewidth, self.pieceheight), self.boardcolor)
        self.load_piece_definitions()

    def load_piece_definitions(self):
        self.MyPieceNameHandler.load_piece_definitions(filename="/home/administrator/chess_variant_boardpainter/shogi_variants/piecedefinitions/chushogipiecedefinitions.csv")
        mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("K")
        assert mytest == "King"
        mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("L")
        assert mytest == "Lance"
        mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol(".")
        assert mytest == ""

    def load_file(self, pfilename):
        self.MyChessPosition.load_from_json(pfilename)

    def boardimage_w_h(self):
        w = self.MyChessPosition.boardwidth * self.piecewidth
        w += self.edgesize_left
        w += self.edgesize_right
        h = self.MyChessPosition.boardheight * self.pieceheight
        h += self.edgesize_top
        h += self.edgesize_bottom
        return w, h

    def prepare_board(self):
        w, h = self.boardimage_w_h()
        self.boardimage = Image.new('RGB', (w, h), self.boardcolor)

    def _load_font(self, size):
        candidates = [
            "arial.ttf",
            "DejaVuSans.ttf",
            "LiberationSans-Regular.ttf",
            "NotoSans-Regular.ttf",
        ]
        for font_name in candidates:
            try:
                return ImageFont.truetype(font_name, size)
            except OSError:
                pass
        return ImageFont.load_default()

    def add_coordinates(self):
        myfontsize = 39 #16
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        draw = ImageDraw.Draw(self.boardimage)
        #font = ImageFont.truetype("arial.ttf", myfontsize)
        font = self._load_font(size=myfontsize)

        for j in range(self.MyChessPosition.boardheight):
            x = (self.MyChessPosition.boardwidth) * self.piecewidth
            x += self.edgesize_left + 12 #5
            rj = (self.MyChessPosition.boardheight - 1) - j
            y = rj * self.pieceheight + (self.pieceheight // 2)
            y += self.edgesize_top
            try:
                myabc = alphabet[rj].upper()
            except:
                myabc = str(rj)
            draw.text((x, y),myabc,(0,0,0),font=font)

        for i in range(self.MyChessPosition.boardwidth):
            ri = self.MyChessPosition.boardwidth - i
            y = 1
            x = i * self.piecewidth
            x += self.edgesize_left + (self.piecewidth // 2)
            draw.text((x, y),str(ri),(0,0,0),font=font)


    def add_gridlines(self):
        draw = ImageDraw.Draw(self.boardimage)
        for j in range(self.MyChessPosition.boardheight + 1):
            y = j * self.pieceheight
            y += self.edgesize_top
            x_start = self.edgesize_left
            x_end = self.edgesize_left + self.MyChessPosition.boardwidth * self.piecewidth
            draw.line([(x_start, y), (x_end, y)], fill="black", width=1)

        for i in range(self.MyChessPosition.boardwidth + 1):
            x = i * self.piecewidth
            x += self.edgesize_left
            y_start = self.edgesize_top
            y_end = self.edgesize_top + self.MyChessPosition.boardheight * self.pieceheight
            draw.line([(x, y_start), (x, y_end)], fill="black", width=1)


    def _symbol_found(self, psymbol: str, ppiecename: str):
        teststring = psymbol.replace("-", "").replace(" ", "").replace(".", "").replace("*", "")
        if teststring != "" and ppiecename == "":
            return False
        return True

    def paste_piece_image(self, j: int, i: int, psymbol: str):
        #For Chu Shogi the square content should end with asterisk (*) to indicate a promoted piece
        #E.g. B = initial Bishop, B* is FL promoted to Bishop
        if psymbol[0] == "-":
            piececolour = "gote"
        else:
            piececolour = "sente"

        if psymbol.endswith("*"):
            ispromoted = True
        else:
            ispromoted = False
        
        mysymbol = psymbol.replace("-", "").replace("*", "")

        piecename = self.MyPieceNameHandler.lookup_piecename_by_symbol(mysymbol)
        symbol_found = self._symbol_found(psymbol=psymbol, ppiecename=piecename)

        x = i * self.piecewidth
        x += self.edgesize_left
        rj = (self.MyChessPosition.boardheight - 1) - j
        y = rj * self.pieceheight
        y += self.edgesize_top

        if symbol_found == False:
            imagefilename = f"_notfound.{self.pieceimages_extension}"
        elif piecename == "":
            imagefilename = f"vacant.{self.pieceimages_extension}"
        elif ispromoted == True:
            imagefilename = f"{piecename.lower()}_{piececolour}_promoted.{self.pieceimages_extension}"
            imagefilename2 = imagefilename
        else:
            imagefilename = f"{piecename.lower()}_{piececolour}.{self.pieceimages_extension}"
            imagefilename2 = f"{piecename.lower()}_{piececolour}_promoted.{self.pieceimages_extension}"

        try:
            try:
                pieceimage = Image.open(f"{self.pieceimages_folder}/{imagefilename}", mode='r')
            except:
                pieceimage = Image.open(f"{self.pieceimages_folder}/{imagefilename2}", mode='r')
        except:
            imagefilename = f"_notfound.{self.pieceimages_extension}"
            pieceimage = Image.open(f"{self.pieceimages_folder}/{imagefilename}", mode='r')

        pieceimage.convert('RGB')
        self.boardimage.paste(pieceimage, (x, y))

    def create_board_image(self):
        self.prepare_board()
        self.add_coordinates()

        for j in range(self.MyChessPosition.boardheight):
            for i in range(self.MyChessPosition.boardwidth):
                symbol = self.MyChessPosition.squares[j][i]
                self.paste_piece_image(j, i, symbol)

        self.add_gridlines()

    def create_board_image_and_save(self, pimagefilename):
        self.create_board_image()
        self.boardimage.save(pimagefilename)
