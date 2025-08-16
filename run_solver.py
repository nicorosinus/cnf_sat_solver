import sys

from sat_solver.io import read_formula_from_stdin
from sat_solver.solver import DPLLSolver



def main() -> int:
    """
    This function starts the process for evaluating the CNF-SAT formula.

    Returns:
        int: 0 if formula is satisfiable, 1 otherwise
    """
    formula = read_formula_from_stdin()
    solver = DPLLSolver()
    model = solver.solve(formula)
    if model is None:
        print("The formula is not satisfiable (UNSAT).")
        return 1
    else:
        if not formula.clauses:
            return 0
        else:
            print("The formula is satisfiable (SAT).\n\nVariable Assignment:")
            for var in sorted(model):
                print(f"  {var} = {model[var]}")
            print("\nIf variables that you typed in are not in the variable assignment, then the satisfiability of the formula is independent from their truth values.")
        return 0



if __name__ == "__main__":
    sys.exit(main())