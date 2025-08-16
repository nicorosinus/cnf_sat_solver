from typing import Dict, Optional, Tuple

from .formula import Formula
from .literals import Literal



class DPLLSolver:
    """
    This class represents the DPLL algorithm for solving a CNF-Sat formula.
    """



    def solve(self, formula: Formula) -> Optional[Dict[str, bool]]:
        """
        This function returns a satisfying assignment, or None if UNSAT.

        Args:
            formula (Formula): CNF-SAT formula
        
        Returns:
            result (Option[Dict[str, bool]]): a satisfying assignment or None if the formula is not satisfiable
        """
        assignment: Dict[str, bool] = {}
        result = self.dpll(formula, assignment)
        return result



    def dpll(self, formula: Formula, assignment: Dict[str, bool]) -> Optional[Dict[str, bool]]:
        """
        This function applies the DPLL algorithm to the CNF-SAT formula.

        Args:
            formula (Formula): CNF-SAT formula
            assignment (Dict[str, bool]): variable assignment

        Returns:
            Optional[Dict[str, bool]]: satisfying assignment if the formula is satisfiable, else None
        """
        formula, assignment, ok = self.simplify(formula, assignment)
        if not ok:
            return None

        val = formula.evaluate(assignment)
        if val is True:
            # Here, it is necessary to assign any missing variables to False for a total assignment.
            total = dict(assignment)
            for v in formula.variables():
                if v not in total:
                    total[v] = False
            return total
        if val is False:
            return None

        var = self.choose_variable(formula, assignment)
        
        for choice in (True, False):
            new_assign = dict(assignment)
            new_assign[var] = choice
            reduced, contradict = formula.reduce({var: choice})
            if contradict:
                continue
            result = self.dpll(reduced, new_assign)
            if result is not None:
                return result
        return None



    def simplify(self, formula: Formula, assignment: Dict[str, bool]) -> Tuple[Formula, Dict[str, bool], bool]:
        """
        This function repeatedly applies Unit Propagation and Pure-Literal elimination.

        Args:
            formula (Formula): CNF-SAT formula
            assignment (Dict[str, bool]): variable assignment

        Returns:
            Tuple[Formula, Dict[str, bool], bool] consisting of (simplified_formula, updated_assignment, ok_flag).
        """
        changed = True
        current_formula = formula
        current_assignment = dict(assignment)

        while changed:
            changed = False

            # unit propagation
            while True:
                units = current_formula.unit_clauses(current_assignment)
                if not units:
                    break
                for cl in units:
                    target: Optional[Literal] = None
                    for lit in cl.literals:
                        if lit.eval(current_assignment) is None:
                            target = lit
                            break
                    assert target is not None
                    current_assignment[target.name] = not target.negated
                    current_formula, contradict = current_formula.reduce({target.name: not target.negated})
                    if contradict:
                        return current_formula, current_assignment, False
                    changed = True

            # pure literal elimination
            pures = current_formula.pure_literals(current_assignment)
            if pures:
                for lit in pures:
                    current_assignment[lit.name] = not lit.negated
                partial = {lit.name: not lit.negated for lit in pures}
                current_formula, contradict = current_formula.reduce(partial)
                if contradict:
                    return current_formula, current_assignment, False
                changed = True

        return current_formula, current_assignment, True



    def choose_variable(self, formula: Formula, assignment: Dict[str, bool]) -> str:
        """
        This function selects the next branching variable for the DPLL algorithm.
        
        The heuristic used is to choose the variable that appears most frequently 
        among undecided literals in the current (partially assigned) formula. 
        
        This increases the likelihood of simplifying the formula quickly.

        Args:
            formula (Formula): CNF-SAT formula
            assignment (Dict[str, bool]): variable assignment

        Returns:
            str: name of the chosen variable to branch on
        """
        counts: Dict[str, int] = {}
        for cl in formula.clauses:
            if cl.evaluate(assignment) is True:
                continue
            for lit in cl.literals:
                if lit.eval(assignment) is None:
                    counts[lit.name] = counts.get(lit.name, 0) + 1
        
        if not counts:
            remaining = formula.variables() - set(assignment.keys())
            return next(iter(remaining))
        return max(counts.items(), key=lambda kv: kv[1])[0]