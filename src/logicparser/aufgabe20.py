from nltk.sem.logic import AndExpression, OrExpression, ImpExpression, IffExpression, NegatedExpression, LogicParser
from numpy.ma.core import true_divide

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
    symbols.sort()

    # --- NEU: Tabellenkopf ausdrucken ---
    header_vars = " | ".join(symbols)
    print(f"\n{header_vars} || KB | Query")
    print("-" * (len(header_vars) + 20))
    # ------------------------------------


    return tt_check_all(kb, exp, symbols, {})

def tt_check_all(kb: KnowledgeBase, exp, symbols, model: dict):
    if len(symbols) == 0:
        kb_true = True
        for satz in kb.sentences:
            if not kb.pl_true(satz, model):
                kb_true = False
                break
        query_true = kb.pl_true(exp, model)

        var_output = " | ".join([f"{k}: {'W' if v else 'F'}" for k, v in sorted(model.items())])

        print(f"{var_output} || KB: {'W' if kb_true else 'F'} | Query: {'W' if query_true else 'F'}")

        if not kb_true:
            return True
        else:
            return query_true

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
    exp_1 = "(A | B | C) & (A | B | -C) & (-A | B | C) & (-A | -B | C)"
    exp_2 = "(A | B | C) & (A | B | -C) & (-A | B | C) & (-A | -B | C)"
    exp_3 = "(A | B | C) & (A | -C) & (-A | B | C | D) & (-A | -B | C)"
    exp_4 = "(A | B | C) & (A | -C) & (-A | (B & C) | D) & (-A | -B | C)"
    exp_5 = "(A | B | C) & (A | -C) & ((-A | B) & (C | D)) & (-A | -B | C)"
    exp_6 = "(A | B | C) & (A | -C) & (((-A | B) & C) | D) & (-A | -B | C)"
    kb.tell(exp_1)
    kb.tell(exp_2)
    kb.tell(exp_3)
    kb.tell(exp_4)
    kb.tell(exp_5)
    kb.tell(exp_6)

    print("Der Satz ist in Knowledgebase: ", tt_entails(kb, expression))
