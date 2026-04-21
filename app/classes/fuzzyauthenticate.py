import re

class FuzzyAthenticate:
    def __init__(self, keywords=""):
        self.set_keywords(inputkeywords=keywords)

    def authenticate(self, inputtext):
        a = re.split(r'[\s,\.]+', inputtext)
        words = []
        for w in a:
            words.append(self.strip_keyword(w))
        # Check if every keyword is present in words
        for keyword in self.keywords:
            if keyword not in words:
                return False
        return True

    def set_keywords(self, inputkeywords):
        a = inputkeywords.split(",")
        self.keywords = []
        for w in a:
            self.keywords.append(self.strip_keyword(w))
        self.keywords = list(set(self.keywords))

    def strip_keyword(self, inputkeyword):
        a = re.sub(r'[^A-Za-z0-9]', '', inputkeyword)
        return a.lower()
