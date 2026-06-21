import config
import os
from app.classes.format_dispatcher import FormatDispatcher
from datetime import datetime

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

def test_classify_input(testfilepath, skip=False):
    if skip == True:
        return
    file1 = open(testfilepath, 'r', encoding='utf-8')
    mytext = file1.read()
    file1.close()
    myinputformat = MyFormatDispatcher.classify_input(inputtext=mytext)
    print(myinputformat)

def test_convert(testfilepath, context, pieceID_separation_strategy, skip=False):
    if skip == True:
        return
    file1 = open(testfilepath, 'r', encoding='utf-8')
    mytext = file1.read()
    file1.close()
    mynewtext = MyFormatDispatcher.convert_format(inputtext=mytext,
                                                  pieceID_separation_strategy=pieceID_separation_strategy,
                                                  context=context)
    print(mynewtext)

def test_make_board(testfilepath, context, theme, skip=False):
    if skip == True:
        return
    file1 = open(testfilepath, 'r', encoding='utf-8')
    mytext = file1.read()
    file1.close()
    file_name = tempfilename()
    jsonfilepath = os.path.join(config.USEROUTPUT_ROOT, "json", f"{file_name}.json")
    imagefilepath = os.path.join(config.USEROUTPUT_ROOT, "boardimages", f"{file_name}.png")
    MyFormatDispatcher.make_board(inputtext=mytext, context=context, theme=theme,
                                  jsonfilepath=jsonfilepath, imagefilepath=imagefilepath)

def tempfilename():
    myfilename_datetimepart = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    myfilename = "usr_pos_" + myfilename_datetimepart
    return myfilename

MyFormatDispatcher = FormatDispatcher()
test_classify_input(testfilepath=testcase_json_filepath(), skip=True)
test_classify_input(testfilepath=shogitestcase_json_filepath(), skip=True)
test_classify_input(testfilepath=testcase_json4_filepath(), skip=True)
test_classify_input(testfilepath=testcase_fen_filepath(), skip=True)
test_classify_input(testfilepath=shogitestcase_fen_filepath(), skip=True)
test_classify_input(testfilepath=testcase_fen4_filepath(), skip=True)

test_convert(testfilepath=testcase_json_filepath(),
             context="chess",
             pieceID_separation_strategy="comma", skip=True)
test_convert(testfilepath=shogitestcase_json_filepath(),
             context="shogi",
             pieceID_separation_strategy="comma", skip=True)
test_convert(testfilepath=testcase_json4_filepath(),
             context="chess",
             pieceID_separation_strategy="comma", skip=True)
test_convert(testfilepath=testcase_fen_filepath(),
             context="chess",
             pieceID_separation_strategy="comma", skip=False)
test_convert(testfilepath=shogitestcase_fen_filepath(),
             context="shogi",
             pieceID_separation_strategy="comma", skip=True)
test_convert(testfilepath=testcase_fen4_filepath(),
             context="chess",
             pieceID_separation_strategy="comma", skip=True)

test_make_board(testfilepath=testcase_json_filepath(),
                context="chess",
                theme="classicwood", skip=True)
test_make_board(testfilepath=testcase_json_filepath(),
                context="chess",
                theme="green", skip=True)
test_make_board(testfilepath=shogitestcase_json_filepath(),
                context="shogi",
                theme="set1", skip=True)
test_make_board(testfilepath=shogitestcase_json_filepath(),
                context="shogi",
                theme="set2", skip=True)
test_make_board(testfilepath=testcase_json4_filepath(),
                context="chess",
                theme="green", skip=True)
test_make_board(testfilepath=testcase_fen_filepath(),
                context="chess",
                theme="classicwood", skip=True)
test_make_board(testfilepath=testcase_fen_filepath(),
                context="chess",
                theme="green", skip=True)
test_make_board(testfilepath=shogitestcase_fen_filepath(),
                context="shogi",
                theme="set1", skip=True)
test_make_board(testfilepath=shogitestcase_fen_filepath(),
                context="shogi",
                theme="set2", skip=True)
test_make_board(testfilepath=testcase_fen4_filepath(),
                context="chess",
                theme="green", skip=True)
