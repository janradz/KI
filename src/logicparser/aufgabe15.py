from nltk.sem.logic import LogicParser

class KnowledgeBase:
    def __init__(self):

        self.parser = LogicParser()
        self.sentences = []

    def tell(self, formel_string):
        parse_exp = self.parser.parse(formel_string)
        self.sentences.append(parse_exp)
        print(f"Erfolgreich hinzugefügt: {parse_exp}")



kb = KnowledgeBase()
exp_1 = "(A & C) -> (B | D)"
exp_2 = "(A & C) <-> (B | D)"
exp_3 = "(A -> C) <-> (B -> D)"
exp_4 = "(A | B) -> (-C & D)"
exp_5 = "A <-> (B & (C | -D))"
kb.tell(exp_1)
kb.tell(exp_2)
kb.tell(exp_3)
kb.tell(exp_4)
kb.tell(exp_5)
