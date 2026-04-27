'''
Local testing of class FENHandler
Without FastAPI
'''
from app.classes.fen_handler import FENHandler
import os
import json

def piecedefinitions_loc():
    s = os.path.join("C:\\", "Users", "Evert Jan", "Documents",
                     "GitHub", "chess_variant_boardpainter",
                     "piecedefinitions", "piecedefinitions.csv")
    return s


def chushogipiecedefinitions_loc():
    s = os.path.join("C:\\", "Users", "Evert Jan", "Documents",
                     "GitHub", "chess_variant_boardpainter", "shogi_variants",
                     "piecedefinitions", "chushogipiecedefinitions.csv")
    return s


def test_parse_one_rank():
    a = myFENHandler.parse_one_rank("rnb3qkbnr")
    assert a == ['r', 'n', 'b', '', '', '', 'q', 'k', 'b', 'n', 'r']
    a = myFENHandler.parse_one_rank("rc,1,b,1,bt,ph,kn,bt,1,b,1,rc")
    assert a == ['rc', '', 'b', '', 'bt', 'ph', 'kn', 'bt', '', 'b', '', 'rc']
    a = myFENHandler.parse_one_rank("rn^Nb~2bqk")
    assert a == ['r', 'n^', 'N', 'b~', '', '', 'b', 'q', 'k']
    a = myFENHandler.parse_one_rank("rn^nb~bq3k")
    assert a == ['r', 'n^', 'n', 'b~', 'b', 'q', '', '', '', 'k']
    a = myFENHandler.parse_one_rank("rN^3nb~bqk")
    assert a == ['r', 'N^', '', '', '', 'n', 'b~', 'b', 'q', 'k']
    a = myFENHandler.parse_one_rank("r3n^nb~bqK:")
    assert a == ['r', '', '', '', 'n^', 'n', 'b~', 'b', 'q', 'K:']
    a = myFENHandler.parse_one_rank("r13n^nb~bqK:")
    assert a == ['r', '', '', '', '', '', '', '', '', '', '', '', '', '', 'n^', 'n', 'b~', 'b', 'q', 'K:']
    a = myFENHandler.parse_one_rank("[r][n^][n][b~][b]qk")
    assert a == ['r', 'n^', 'n', 'b~', 'b', 'q', 'k']
    a = myFENHandler.parse_one_rank("[AX][2][BX][CX][DX][EX]2[FX]")
    assert a == ['AX', '2', 'BX', 'CX', 'DX', 'EX', '', '', 'FX']
    a = myFENHandler.parse_one_rank("r,3,n^,n,b~,b,q,k")
    assert a == ['r', '', '', '', 'n^', 'n', 'b~', 'b', 'q', 'k']
    a = myFENHandler.parse_one_rank("r,3,n^,n,b~,b,11,q,k")
    assert a == ['r', '', '', '', 'n^', 'n', 'b~', 'b', '', '', '', '', '', '', '', '', '', '', '', 'q', 'k']
    a = myFENHandler.parse_one_rank("r,3,n^,n,b~,b,11,q,kn")
    assert a == ['r', '', '', '', 'n^', 'n', 'b~', 'b', '', '', '', '', '', '', '', '', '', '', '', 'q', 'kn']
    a = myFENHandler.parse_one_rank("[r][n^]2[N]e,12,fg,H7,IJ,[b~][b]qk")
    assert a == ['r', 'n^', '', '', 'N', 'e',
                '', '', '', '', '', '', '', '', '', '', '', '',
                'fg', 'H7', 'IJ', 'b~', 'b', 'q', 'k']

def testcase_FEN(filename):
    testcasespath = os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                     "chesspython_nogithub", "positions", "testcases_fen",
                     filename)
    testcasespathcheck = os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                     "chesspython_nogithub", "positions", "testcases_fen",
                     "check", filename)
    file1 = open(testcasespath, 'r')
    myjson = json.load(file1)
    myjsontext = json.dumps(myjson, indent=4)
    file1.close()

    myfen = myFENHandler.convert_JSON_to_fen(jsontext=myjsontext)

    a = myFENHandler.detect_JSON(inputtext=myjsontext)
    print(f"JSON detection result {a}")
    a = myFENHandler.detect_JSON(inputtext=myfen)
    print(f"JSON detection result {a}")

    rc, myjson2 = myFENHandler.convert_fen_to_JSON(fentext=myfen)
    assert rc == 0

    file2 = open(testcasespathcheck, 'w', encoding='utf-8')
    file2.write(myjson2)
    file2.close()

    print(filename)
    print(myfen)
    return myjsontext

fen0 = '{ "mypiece": "King"}'
fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen2 = "4k2r/8/8/8/1Pp5/8/8/5K2 b k b3 0 1"
fen3 = "rn^nb~bqkbr~nn^r/pppppppppppp/12/12/12/12/12/12/12/12/PPPPPPPPPPPP/RN^NB~BQKBR~NN^R"
fen4 = "l,fl,c,s,g,de,k,g,s,c,fl,l/rc,1,b,1,bt,ph,kr,bt,1,b,1,rc/sm,vm,r,dh,dk,q,ln,dk,dh,r,vm,sm/p,p,p,p,p,p,p,p,p,p,p,p/3,gb,4,gb,3/12/"
fen4 += "12/3,GB,4,GB,3/P,P,P,P,P,P,P,P,P,P,P,P/SM,VM,R,DH,DK,Q,LN,DK,DH,R,VM,SM/RC,1,B,1,BT,PH,KR,BT,1,B,1,RC/L,FL,C,S,G,DE,K,G,S,C,FL,L w"
fen5 = "[l][fl][c][s][g][de][k][g][s][c][fl][l]/[rc]1[b]1[bt][ph][kr][bt]1[b]1[rc]/[sm][vm][r][dh][dk][q][ln][dk][dh][r][vm][sm]/[p][p][p][p][p][p][p][p][p][p][p][p]/3[gb]4[gb]3/12/"
fen5 += "12/3[GB]4[GB]3/[P][P][P][P][P][P][P][P][P][P][P][P]/[SM][VM][R][DH][DK][Q][LN][DK][DH][R][VM][SM]/[RC]1[B]1[BT][PH][KR][BT]1[B]1[RC]/[L][FL][C][S][G][DE][K][G][S][C][FL][L] w"

#We pick a location and filename for the piecedefinitions.csv

#We load the piecedefinitions.csv

myFENHandler = FENHandler(piecedefinitions_loc=piecedefinitions_loc())
myFENHandler.load_piece_definitions()
test_parse_one_rank()

#a = myFENHandler.convert_JSON_to_fen(jsontext=json_input_testcase3())
#rc, myjson = myFENHandler.convert_fen_to_JSON(fentext=a)

myjson = testcase_FEN(filename="testcase_FEN_chess_01_simple.json")
myjson = testcase_FEN(filename="testcase_FEN_chess_02_simple_special_nonalf.json")
myFENHandler.pieceID_separation_strategy = "comma"
myjson = testcase_FEN(filename="testcase_FEN_chess_03_comma.json")
myFENHandler.pieceID_separation_strategy = "squarebracket"
myjson = testcase_FEN(filename="testcase_FEN_chess_04_squarebrackets.json")
del myFENHandler
myFENHandler = FENHandler(piecedefinitions_loc=chushogipiecedefinitions_loc())
myFENHandler.load_piece_definitions()
myjson = testcase_FEN(filename="testcase_FEN_chu_01_simple.json")
myjson = testcase_FEN(filename="testcase_FEN_chu_02_simple_special_nonalf.json")
myFENHandler.pieceID_separation_strategy = "comma"
myjson = testcase_FEN(filename="testcase_FEN_chu_03_comma.json")
myFENHandler.pieceID_separation_strategy = "squarebracket"
myjson = testcase_FEN(filename="testcase_FEN_chu_04_squarebrackets.json")
