from nltk.sem.logic import AndExpression, OrExpression, ImpExpression, IffExpression, NegatedExpression, LogicParser

from logicparser.aufgabe16 import KnowledgeBase


def extract_symbols(symbols, exp):

    if isinstance(exp, (AndExpression, OrExpression, ImpExpression, IffExpression)):
        extract_symbols(symbols,exp.first)
        extract_symbols(symbols,exp.second)
    elif isinstance(exp, NegatedExpression):
        extract_symbols(symbols,exp.term)
    else:
        # Basisfall: Atomare Variable
        var_name = str(exp)
        if var_name not in symbols:
            symbols.append(var_name)


def tt_entails(kb: KnowledgeBase, exp):
    if isinstance(exp, str):
        parser_int = LogicParser()
        # exp zuerst parsen!
        exp = parser_int.parse(exp)

    symbols_alpha = []
    extract_symbols(symbols_alpha, exp)
    symbols = list(set(kb.symbols + symbols_alpha))


    return tt_check_all(kb, exp, symbols, {})

def tt_check_all(kb: KnowledgeBase, exp, symbols, model: dict):
    if len(symbols) == 0:
        for satz in kb.sentences:
            if not kb.pl_true(satz, model):
                return True
        else:
            return kb.pl_true(exp, model)
    else:
        # Statt pop() - verwende Slicing, um die Liste nicht zu modifizieren!
        p = symbols[0]
        rest = symbols[1:]
        return (tt_check_all(kb, exp, rest, {**model, p: True}) and
                tt_check_all(kb, exp, rest, {**model, p: False}))

if __name__ == "__main__":
    parser = LogicParser()
    expression_str = "B | E"
    print("zu prüfender Satz: ", expression_str)
    expression = parser.parse(expression_str)
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

    print("Der Satz ist in Knowledgebase: ", tt_entails(kb, expression))
