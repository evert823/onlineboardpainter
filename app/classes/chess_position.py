import json

class ChessPosition:
    def __init__(self):
        self.boardwidth = -1
        self.boardheight = -1
        self.squares = []
        self.terrain = []
        self.reset_boardsize(0, 0)

    def reset_boardsize(self, pboardwidth, pboardheight):
        self.boardwidth = pboardwidth
        self.boardheight = pboardheight
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
        self.boardwidth = positiondict["boardwidth"]
        self.boardheight = positiondict["boardheight"]
        self.reset_boardsize(self.boardwidth, self.boardheight)
        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            mysymbol = positiondict["squares"][rj].split("|")
            for i in range(self.boardwidth):
                s = mysymbol[i].lstrip()
                self.squares[j][i] = s

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
            for i in range(self.boardwidth):
                print(self.squares[j][i])
