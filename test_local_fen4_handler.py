from app.classes.fen4_handler import FEN4Handler
import config
import os

def piecedefinitions_loc():
    s = os.path.join(config.RESOURCES_ROOT, "piecedefinitions", "piecedefinitions.csv")
    return s

def testfenfilepath(filename):
    return os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                        "chesspython_nogithub", "fen", filename)

def testjsonfilepath(filename):
    return os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                        "chesspython_nogithub", "positions", filename)

def testfen2json(testfilepath):
    file1 = open(testfilepath, 'r', encoding='utf-8')
    myfen = file1.read()
    print(myfen)
    rc, myjson = myFEN4Handler.convert_fen_to_JSON(fentext=myfen)
    assert rc == 0
    print(myjson)

def testjson2fen(testfilepath):
    file1 = open(testfilepath, 'r', encoding='utf-8')
    myjsontext = file1.read()
    print(myjsontext)
    myfen = myFEN4Handler.convert_JSON_to_fen(jsontext=myjsontext)
    print(myfen)

myFEN4Handler = FEN4Handler(piecedefinitions_loc=piecedefinitions_loc())
myFEN4Handler.load_piece_definitions()

testfen2json(testfilepath=testfenfilepath(filename="somefen4.txt"))
#testjson2fen(testfilepath=testjsonfilepath(filename="bulldog_4player.json"))
