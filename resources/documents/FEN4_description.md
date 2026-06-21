# Description of FEN4 representation for 4 player chess positions

# Source
We haven't yet found an official source that describes FEN4.
The description provided here matches what we see on chess.com

# Representation of a commonly used standard position on a 14x14 board
R-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-
3,yR,yN,yB,yK,yQ,yB,yN,yR,3/
3,yP,yP,yP,yP,yP,yP,yP,yP,3/
14/
bR,bP,10,gP,gR/
bN,bP,10,gP,gN/
bB,bP,10,gP,gB/
bQ,bP,10,gP,gK/
bK,bP,10,gP,gQ/
bB,bP,10,gP,gB/
bN,bP,10,gP,gN/
bR,bP,10,gP,gR/
14/
3,rP,rP,rP,rP,rP,rP,rP,rP,3/
3,rR,rN,rB,rQ,rK,rB,rN,rR,3

# Description
The first line contains 6 fields separated by hyphens:
- Player to move (one upper case letter: R, B, Y or G for red, blue, yellow and green respectively)
- Four flags indicating eliminated players
- Four flags indicating Kingside castling rights
- Four flags indicating Queenside castling rights
- Four point counters
- Halfmove clock

The subsequent lines contain the piece placements. There is one line for each rank, so there are 14 lines for a 14x14 board.
The lines for piece placements are similar to standard FEN, with two differences:
- The piece symbol is always upper case
- The piece symbol is prefixed by a lower case letter for the color (r, b, y, g)
