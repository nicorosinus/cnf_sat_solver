from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, Optional, Set, Tuple

from .clauses import Clause
from .literals import Literal



@dataclass(frozen=True)
class Formula:
    """
    This class represents a CNF formula, that is a conjunction (AND) of clauses.
    
    Args:
        clauses (FrozenSet[Clause]): clause set
    """
    clauses: FrozenSet[Clause]



    @staticmethod
    def of(clauses: Iterable[Clause]) -> "Formula":
        """
        This function builds a formula from an Iterable-object of clauses.

        Args:
            clauses (Iterable[Clause]): clauses of the formula

        Returns:
            formula of clauses (of datatype Formula(frozenset(clauses)))
        """
        normalized: Set[Clause] = set()
        for cl in clauses:
            names_to_signs: Dict[str, Set[bool]] = {}
            for lit in cl.literals:
                names_to_signs.setdefault(lit.name, set()).add(lit.negated)
            if any(len(signs) == 2 for signs in names_to_signs.values()):
                # if clause consist of a literal and it's negation, it is always true.
                continue
            normalized.add(cl)
        return Formula(frozenset(normalized))



    def variables(self) -> Set[str]:
        """
        This function returns the literal names from the formula.

        Returns:
            set[str]: literal names of formula
        """
        return {lit.name for clause in self.clauses for lit in clause.literals}



    def evaluate(self, assignment: Dict[str, bool]) -> Optional[bool]:
        """
        This function evaluates a formula under an assignment.

        Args:
            assignment (Dict[str, bool]): variable assignment

        Returns:
            True if all clauses True
            OR
            False if any clause False
            OR
            None otherwise
        """
        undecided = False
        for cl in self.clauses:
            val = cl.evaluate(assignment)
            if val is False:
                return False
            if val is None:
                undecided = True
        return True if not undecided else None



    def unit_clauses(self, assignment: Dict[str, bool]) -> Set[Clause]:
        """
        This function calculates the unit-clauses of the formula.

        Args:
            assignment (Dict[str, bool]): variable assignment

        Returns:
            Set[Clause]: set of  unit-clauses
        """
        return {cl for cl in self.clauses if cl.is_unit(assignment)}



    def pure_literals(self, assignment: Dict[str, bool]) -> Set[Literal]:
        """
        This function finds pure literals among currently undecided occurrences.

        Args:
            assignment (Dict[str, bool]): variable assignment

        Returns:
            Set[Literal]: pure literals of formula
        """
        sign_by_var: Dict[str, Set[bool]] = {}
        for cl in self.clauses:
            cl_val = cl.evaluate(assignment)
            if cl_val is True:
                continue
            for lit in cl.literals:
                if lit.eval(assignment) is None:
                    sign_by_var.setdefault(lit.name, set()).add(lit.negated)
        pures: Set[Literal] = set()
        for var, signs in sign_by_var.items():
            if len(signs) == 1:
                only_negated = next(iter(signs))
                pures.add(Literal(var, only_negated))
        return pures



    def reduce(self, assignment: Dict[str, bool]) -> Tuple["Formula", bool]:
        """
        This function applies the assignment to all clauses and returns a tuple indicating the 
        (reduced_formula, contradiction_flag). If any clause becomes empty -> contradiction_flag=True.

        Args:
            assignment (Dict[str, bool]): variable assignment

        Returns:
            Tuple[Formula, bool]: tuple of reduced formula and contradiction flag
        """
        new_clauses: Set[Clause] = set()
        for cl in self.clauses:
            red = cl.reduce(assignment)
            if red is None:
                continue
            if red.is_empty():
                return Formula(frozenset()), True
            new_clauses.add(red)
        return Formula(frozenset(new_clauses)), False



    def __str__(self) -> str:
        """
        This function produces the string representation of a whole formula.

        Returns:
            f-string representing the whole formula
        """
        if not self.clauses:
            return "⊤"
        return " ∧ ".join(f"({cl})" for cl in sorted(self.clauses, key=lambda c: sorted((l.name, l.negated) for l in c.literals)))