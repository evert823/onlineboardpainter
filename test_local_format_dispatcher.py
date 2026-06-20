import config
import os
from app.classes.format_dispatcher import FormatDispatcher
from app.models.fen_json_converter_input import FENJsonConverterInput

def testcase_json_filepath():
    return os.path.join(config.RESOURCES_ROOT, "position_json_examples",
                     "personA_personB.json")

def shogitestcase_json_filepath():
    return os.path.join(config.RESOURCES_ROOT, "position_json_examples",
                     "shogi_variants", "chu_shogi_initial_position.json")

def testcase_json4_filepath():
    return os.path.join(config.RESOURCES_ROOT, "position_json_examples",
                     "bulldog_4player.json")

def testcase_fen_filepath():
    return os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                     "chesspython_nogithub", "fen", "somefen.txt")

def shogitestcase_fen_filepath():
    return os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                     "chesspython_nogithub", "fen", "somechufen.txt")

def testcase_fen4_filepath():
    return os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects",
                     "chesspython_nogithub", "fen", "somefen4.txt")

def test_classify_input(testfilepath):
    file1 = open(testfilepath, 'r', encoding='utf-8')
    mytext = file1.read()
    file1.close()
    myinputformat = MyFormatDispatcher.classify_input(inputtext=mytext)
    print(myinputformat)

def test_convert(testfilepath, context, pieceID_separation_strategy):
    file1 = open(testfilepath, 'r', encoding='utf-8')
    mytext = file1.read()
    file1.close()
    myinput = FENJsonConverterInput(context=context,
                                    text=mytext,
                                    direction="fen2json", #we will no longer need this
                                    pieceID_separation_strategy=pieceID_separation_strategy)
    mynewtext = MyFormatDispatcher.convert_format(input=myinput)
    print(mynewtext)

MyFormatDispatcher = FormatDispatcher()
test_classify_input(testfilepath=testcase_json_filepath())
test_classify_input(testfilepath=shogitestcase_json_filepath())
test_classify_input(testfilepath=testcase_json4_filepath())
test_classify_input(testfilepath=testcase_fen_filepath())
test_classify_input(testfilepath=shogitestcase_fen_filepath())
test_classify_input(testfilepath=testcase_fen4_filepath())

test_convert(testfilepath=testcase_json_filepath(),
             context="chess",
             pieceID_separation_strategy="comma")
test_convert(testfilepath=shogitestcase_json_filepath(),
             context="shogi",
             pieceID_separation_strategy="comma")
test_convert(testfilepath=testcase_json4_filepath(),
             context="chess",
             pieceID_separation_strategy="comma")
test_convert(testfilepath=testcase_fen_filepath(),
             context="chess",
             pieceID_separation_strategy="comma")
test_convert(testfilepath=shogitestcase_fen_filepath(),
             context="shogi",
             pieceID_separation_strategy="comma")
test_convert(testfilepath=testcase_fen4_filepath(),
             context="chess",
             pieceID_separation_strategy="comma")
