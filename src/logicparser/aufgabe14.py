from nltk.sem.logic import LogicParser


def print_tree(node, depth=0):
    """Gibt den kompletten Aufrufsbaum rekursiv aus"""
    indent = "  " * depth
    print(f"{indent}{type(node).__name__}: {node}")

    # Rekursiv durch die Kinder gehen
    if hasattr(node, 'first'):
        print(f"{indent}├─ first:")
        print_tree(node.first, depth + 2)

    if hasattr(node, 'second'):
        print(f"{indent}└─ second:")
        print_tree(node.second, depth + 2)


lp = LogicParser()

formel_string = "(A | B | C) & (A | B | -C) & (-A | B | C) & (-A | -B | C)"

parse_tree = lp.parse(formel_string)

print("Kompletter Aufrufsbaum:")
print("=" * 50)
print_tree(parse_tree)
