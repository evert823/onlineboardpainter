from app.models.text_input import TextInput
from app.classes.fuzzyauthenticate import FuzzyAthenticate

def verify_test_text(input: TextInput):
    # Your logic here
    myfa = FuzzyAthenticate(keywords=get_keywords_from_file())
    myresult = myfa.authenticate(inputtext=input.text)
    if myresult:
        return {"success": True, "message": "Authenticated!"}
    else:
        return {"success": False, "message": "Authentication failed."}

def get_keywords_from_file():
    filepath = "/home/administrator/onlineboardpainter/apikeywords.txt"
    file1 = open(filepath, "r", encoding="utf-8")
    keywords = file1.read().strip()
    file1.close()
    return keywords
