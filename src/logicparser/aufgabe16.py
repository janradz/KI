from operator import neg

from nltk.parse.chart import LeafEdge
from nltk.sem.logic import LogicParser, AndExpression, OrExpression, NegatedExpression, ImpExpression, \
    EqualityExpression, IffExpression

m = {'A': True, 'B': True, 'C': False, 'D': False}

class KnowledgeBase:
    def __init__(self):

        self.parser = LogicParser()
        self.sentences = []
        self.symbols = []

    def tell(self, formel_string):
        parse_exp = self.parser.parse(formel_string)
        self.sentences.append(parse_exp)
        # Variablen aus dem Ausdruck extrahieren und zu symbols hinzufügen
        self._extract_symbols(parse_exp)
        print(f"Erfolgreich hinzugefügt: {parse_exp}")

    def _extract_symbols(self, exp):
        """Extrahiert alle Variablen aus einem logischen Ausdruck"""
        if isinstance(exp, (AndExpression, OrExpression, ImpExpression, IffExpression)):
            self._extract_symbols(exp.first)
            self._extract_symbols(exp.second)
        elif isinstance(exp, NegatedExpression):
            self._extract_symbols(exp.term)
        else:
            # Basisfall: Atomare Variable
            var_name = str(exp)
            if var_name not in self.symbols:
                self.symbols.append(var_name)

    def pl_true(self, exp, model):
        """
         Wertet einen logischen Ausdruck (expression) basierend auf einem
         Dictionary von Wahrheitswerten (model) aus.
        """
        if isinstance(exp, AndExpression):
            left = self.pl_true(exp.first, model)
            right = self.pl_true(exp.second, model)
            return left and right
        elif isinstance(exp, OrExpression):
            left = self.pl_true(exp.first, model)
            right = self.pl_true(exp.second, model)
            return left or right
        elif isinstance(exp, NegatedExpression):
            val = self.pl_true(exp.term, model)
            return not val

        elif isinstance(exp, ImpExpression):
            prem = self.pl_true(exp.first, model)
            concl = self.pl_true(exp.second, model)
            if prem and not concl:
                return False
            else:
                return True
        elif isinstance(exp, IffExpression):
            left = self.pl_true(exp.first, model)
            right = self.pl_true(exp.second, model)
            return left == right
        else:
            # Base Case: Wenn es keiner der Operatoren ist, MUSS es die Variable sein
            var_name = str(exp)
            return model[var_name]





if __name__ == "__main__":
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


    print("\n--- Auswertung der Knowledge Base ---")
    for satz in kb.sentences:
        # Hier rufen wir deine rekursive Funktion für jeden Satz auf
        ergebnis = kb.pl_true(satz, m)

        # Ausgabe des Resultats, wie in der Aufgabe gefordert
        print(f"Satz: {satz}")
        print(f"Wahrheitswert im Modell: {ergebnis}")
        print("-" * 30)
