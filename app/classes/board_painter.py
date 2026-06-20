from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from app.classes.chess_position import ChessPosition
from app.classes.piece_name_handler import PieceNameHandler

class BoardPainter:
    def __init__(self):
        self.MyChessPosition = ChessPosition()
        self.MyPieceNameHandler = PieceNameHandler()
        self.pieceimages_folder = "pieceimages"
        self.pieceimages_extension = "jpg"
        self.a1_is_white = True
        self.piecesize = 57
        self.edgesize_top = 6
        self.edgesize_bottom = 24
        self.edgesize_left = 22
        self.edgesize_right = 6
        self.boardimage = Image.new('RGB', (self.piecesize, self.piecesize), (0, 0, 0))
        self.load_piece_definitions()

    def load_piece_definitions(self):
        self.MyPieceNameHandler.load_piece_definitions()
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol("K")
        assert symbol_found == True and mytest == "King"
        symbol_found, mytest = self.MyPieceNameHandler.lookup_piecename_by_symbol(".")
        assert symbol_found == True and mytest == ""

    def load_file(self, pfilename):
        self.MyChessPosition.load_from_json(pfilename)

    def boardimage_w_h(self):
        w = self.MyChessPosition.boardwidth * self.piecesize
        w += self.edgesize_left
        w += self.edgesize_right
        h = self.MyChessPosition.boardheight * self.piecesize
        h += self.edgesize_top
        h += self.edgesize_bottom
        return w, h

    def prepare_board(self):
        w, h = self.boardimage_w_h()
        self.boardimage = Image.new('RGB', (w, h), (0, 0, 0))

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
        myfontsize = 16
        if self.MyChessPosition.boardheight > 9:
            myfontsize = 13

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        draw = ImageDraw.Draw(self.boardimage)
        #font = ImageFont.truetype("arial.ttf", myfontsize)
        font = self._load_font(size=myfontsize)

        for j in range(self.MyChessPosition.boardheight):
            rj = (self.MyChessPosition.boardheight - 1) - j
            y = rj * self.piecesize
            y += self.edgesize_top
            y += 21
            draw.text((5, y),str(j + 1),(255,255,255),font=font)

        for i in range(self.MyChessPosition.boardwidth):
            y = (self.MyChessPosition.boardheight) * self.piecesize
            y += self.edgesize_top
            x = i * self.piecesize
            x += self.edgesize_left
            x += 23
            try:
                myabc = alphabet[i]
            except:
                myabc = str(i)
            draw.text((x, y),myabc,(255,255,255),font=font)

    def get_squarecolour(self, j: int, i: int) -> str:
        if self.a1_is_white:
            mydummy: int = 0
        else:
            mydummy: int = 1

        if (i + j + mydummy) % 2 == 0:
            return "white"
        else:
            return "black"

    def parse_piece_identifier(self, psymbol):
        clean_symbol = psymbol.strip()
        clean_symbol = clean_symbol.replace(" ", "")
        clean_symbol = clean_symbol.replace("\t", "")
        if clean_symbol.find("-") > -1:
            armyid = "black"
            pieceid = clean_symbol.replace("-", "")
            return armyid, pieceid
        if clean_symbol.find(".") < 0:
            armyid = "white"
            pieceid = clean_symbol
            return armyid, pieceid
        a = clean_symbol.split(".")
        mapping = {"we": "white",
                   "bk": "black",
                   "be": "blue",
                   "gn": "green",
                   "rd": "red",
                   "yw": "yellow"}
        armyid = mapping.get(a[0].lower())
        pieceid = a[1]
        return armyid, pieceid

    def paste_piece_image(self, j: int, i: int):
        mysquare = self.MyChessPosition.squares[j][i]
        piececolour, symbol2 = self.parse_piece_identifier(psymbol=mysquare)
        try:
            myterrain = self.MyChessPosition.terrain[j][i]
        except:
            myterrain = ""

        if myterrain == "DF":
            myextension = "jpg"
            myfolder = "pieceimages"
        elif piececolour in ['blue', 'green', 'red', 'yellow']:
            myextension = "jpg"
            myfolder = "othercolors_theme_green"
        else:
            myextension = self.pieceimages_extension
            myfolder = self.pieceimages_folder

        symbol_found, piecename = self.MyPieceNameHandler.lookup_piecename_by_symbol(symbol2)

        x = i * self.piecesize
        x += self.edgesize_left
        rj = (self.MyChessPosition.boardheight - 1) - j
        y = rj * self.piecesize
        y += self.edgesize_top

        squarecolour = self.get_squarecolour(i, j)

        if symbol_found == False:
            imagefilename = f"_notfoundon{squarecolour}.{myextension}"
        elif piecename == "":
            imagefilename = f"vacanton{squarecolour}.{myextension}"
        else:
            imagefilename = f"{piececolour}{piecename.lower()}on{squarecolour}.{myextension}"

        try:
            pieceimage = Image.open(f"/home/administrator/onlineboardpainter/resources/{myfolder}/{imagefilename}", mode='r')
        except:
            imagefilename = f"_notfoundon{squarecolour}.{myextension}"
            pieceimage = Image.open(f"/home/administrator/onlineboardpainter/resources/{myfolder}/{imagefilename}", mode='r')

        pieceimage.convert('RGB')

        # Draw dot for terrain if needed
        if myterrain in ["h1", "h2"]:
            draw = ImageDraw.Draw(pieceimage)
            ps = self.piecesize
            radius = int(ps * 0.15)
            # Place dot in the right top corner, with a small margin
            margin = int(ps * 0.05)
            center = (ps - margin - radius, margin + radius)
            if myterrain == "h1":
                dot_color = (255, 0, 0)  # red
            else:
                dot_color = (255, 255, 255)  # white
            draw.ellipse(
                [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
                fill=dot_color, outline=None)

        self.boardimage.paste(pieceimage, (x, y))

    def create_board_image(self):
        self.prepare_board()
        self.add_coordinates()

        for j in range(self.MyChessPosition.boardheight):
            for i in range(self.MyChessPosition.boardwidth):
                self.paste_piece_image(j, i)

    def create_board_image_and_save(self, pimagefilename):
        self.create_board_image()
        self.boardimage.save(pimagefilename)
