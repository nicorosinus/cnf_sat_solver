from typing import Set

from .clauses import Clause
from .formula import Formula
from .literals import Literal



def parse_clause(line: str) -> Clause:
    """
    This function parses a single line into a Clause.
    Tokens are separated by whitespace. Negations allowed via - prefix.
    Example: "A -B C"  <=> (A ∨ ¬B ∨ C)

    Args:
        line (str): read line from stdin

    Returns:
        clause of read input
    """
    tokens = [tok for tok in line.strip().split() if tok]
    lits: Set[Literal] = set()
    for tok in tokens:
        negated = False
        name = tok
        if tok.startswith("-"):
            negated = True
            name = tok[len("-"):]
        lits.add(Literal(name=name, negated=negated))
    return Clause.of(lits)



def read_formula_from_stdin() -> Formula:
    """
    This function reads the input from stdin.

    Returns:
        Formula: CNF-SAT formula read from stdin
    """
    print("Welcome to the CNF-SAT Solver!\nPlease type in your formula.\n\nExamples:")
    print("  A B C       is equivalent to (A ∨ B ∨ C)")
    print("  A -B        is equivalent to (A ∨ ¬B)")
    print("  An empty line ends the process.\n")

    clauses: Set[Clause] = set()
    while True:
        try:
            line = input("> ").strip()
        except:
            break
        if not line:
            break
        clause = parse_clause(line)
        clauses.add(clause)

    formula = Formula.of(clauses)
    if not formula.clauses:
        print("The fomula is empty and therefore satisfiable (⊤).")
    else:
        print("\nFormula:", formula, "\n")
    return formula