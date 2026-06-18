import json

class ChessPosition:
    def __init__(self):
        self.boardwidth = -1
        self.boardheight = -1
        self.colourtomove = 1
        self.squares = []
        self.terrain = []
        self.reset_boardsize(0, 0)

    def reset_boardsize(self, pboardwidth, pboardheight):
        self.boardwidth = pboardwidth
        self.boardheight = pboardheight
        if self.boardwidth > 600:
            raise ValueError("boardsize not allowed")
        if self.boardheight > 600:
            raise ValueError("boardsize not allowed")
        self.squares.clear()
        self.terrain = []
        for j in range(self.boardheight):
            myrank = []
            for i in range(self.boardwidth):
                myrank.append("")
            self.squares.append(myrank)

    def load_from_json(self, pfilename):
        #Load from json file and convert to class structure
        positionfile = open(pfilename, 'r')
        positiondict = json.load(positionfile)
        positionfile.close()
        self.load_from_dict(positiondict=positiondict)

    def load_from_jsontext(self, jsontext):
        #Load from json file and convert to class structure
        positiondict = json.loads(jsontext)
        self.load_from_dict(positiondict=positiondict)

    def load_from_dict(self, positiondict):
        #Load from json file and convert to class structure
        self.boardwidth = positiondict["boardwidth"]
        self.boardheight = positiondict["boardheight"]
        self.reset_boardsize(self.boardwidth, self.boardheight)
        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            mysymbol = positiondict["squares"][rj].split("|")
            for i in range(self.boardwidth):
                s = mysymbol[i].lstrip()
                self.squares[j][i] = s

        if "colourtomove" in positiondict:
            self.colourtomove = positiondict["colourtomove"]

        # Parse terrain if present
        if "terrain" in positiondict:
            self.terrain = []
            for j in range(self.boardheight):
                rj = (self.boardheight - 1) - j
                myterrain = positiondict["terrain"][rj].split("|")
                row = []
                for i in range(self.boardwidth):
                    t = myterrain[i].lstrip()
                    row.append(t)
                self.terrain.append(row)
            #print("TERRAIN:")
            #self.print_terrain()

    def print_terrain(self):
        for j in range(len(self.terrain)):
            print(",".join(self.terrain[j]))

    def print_squares(self):
        for j in range(self.boardheight):
            print(self.squares[j])

    def max_len_symbol(self):
        mymax = -1
        for j in range(self.boardheight):
            for i in range(self.boardwidth):
                if len(self.squares[j][i]) > mymax:
                    mymax = len(self.squares[j][i])
        return mymax
