from nltk.sem.logic import LogicParser
from nltk.sem.evaluate import Valuation, Model, Assignment


class KnowledgeBase:
    def __init__(self):
        self.parser = LogicParser()
        self.sentences = []

    def tell(self, formel_string):
        parse_exp = self.parser.parse(formel_string)
        self.sentences.append(parse_exp)


kb = KnowledgeBase()
kb.tell("(A & C) -> (B | D)")
kb.tell("(A & C) <-> (B | D)")
kb.tell("(A -> C) <-> (B -> D)")
kb.tell("(A | B) -> (-C & D)")
kb.tell("A <-> (B & (C | -D))")

#NLTK Setup
nltk_werte = [('A', True), ('B', True), ('C', False), ('D', False)]
val = Valuation(nltk_werte)
dom = set()
nltk_model = Model(dom, val)
g = Assignment(dom)

#NLTK auswertung
print("\n--- Auswertung P17 (NLTK PL-True) ---")
for satz in kb.sentences:
    #nltk braucht den satz als string für .evaluate()
    nltk_ergebnis = nltk_model.evaluate(str(satz), g)

    print(f"Satz: {satz}")
    print(f"Wahrheitswert im Modell (NLTK): {nltk_ergebnis}")
    print("-" * 30)