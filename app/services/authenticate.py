from app.models.text_input import TextInput
from app.classes.fuzzyauthenticate import FuzzyAthenticate

def verify_test_text(input: TextInput):
    # Your logic here
    myfa = FuzzyAthenticate(keywords="norrell,strange")
    myresult = myfa.authenticate(inputtext=input.text)
    if myresult:
        return {"success": True, "message": "Authenticated!"}
    else:
        return {"success": False, "message": "Authentication failed."}
