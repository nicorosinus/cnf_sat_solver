from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, Optional, Set

from .literals import Literal



@dataclass(frozen=True)
class Clause:
    """
    Tis class represents a clause, that is a disjunction (OR) of literals.
    
    Args:
        literals (FrozenSet[Literal]): set of literals per clause
    """
    literals: FrozenSet[Literal]



    @staticmethod
    def of(lits: Iterable[Literal]) -> "Clause":
        """
        This function builds a clause from an Iterable-object of literals.

        Args:
            lits (Iterable[Literal]): literals of the clause

        Returns:
            clause of literals (of datatype Clause(frozenset(literals)))
        """
        lits_set: Set[Literal] = set(lits)
        names_to_signs: Dict[str, Set[bool]] = {}
        for lit in lits_set:
            names_to_signs.setdefault(lit.name, set()).add(lit.negated)
        for signs in names_to_signs.values():
            if len(signs) == 2:
                # if clause consist of a literal and it's negation, it is always true.
                pass
        return Clause(frozenset(lits_set))



    def is_empty(self) -> bool:
        """
        This function checks weather the clause is empty.

        Returns:
            boolean that indicates weather the clause is empty or not
        """
        return len(self.literals) == 0



    def is_unit(self, assignment: Dict[str, bool]) -> bool:
        """
        This function checks weather the clause is an unit-clause.

        Args:
            assignment (Dict[str, bool]): variable assignment

        Returns:
            True if clause is a unit-clause, otherwise False
        """
        undecided = 0
        for lit in self.literals:
            val = lit.eval(assignment)
            if val is True:
                return False
            if val is None:
                undecided += 1
                if undecided > 1:
                    return False
        return undecided == 1



    def evaluate(self, assignment: Dict[str, bool]) -> Optional[bool]:
        """
        This function evaluates the clause under an assignment.

        Args:
            assignment (Dict[str, bool]): variable assignment
        
        Returns:
            True if any literal is True
            OR
            False if all literals are False
            OR
            None if undecided
        """
        undecided = False
        for lit in self.literals:
            val = lit.eval(assignment)
            if val is True:
                return True
            if val is None:
                undecided = True
        return None if undecided else False



    def reduce(self, assignment: Dict[str, bool]) -> Optional["Clause"]:
        """
        This function applies an assignment. 
        
        Args:
            assignment (Dict[str, bool]): variable assignment

        Returns:
            None if clause is satisfied (drop clause)
            OR
            new clause with falsified literals removed
        """
        new_lits: Set[Literal] = set()
        for lit in self.literals:
            val = lit.eval(assignment)
            if val is True:
                return None
            if val is None:
                new_lits.add(lit)
        return Clause(frozenset(new_lits))



    def __str__(self) -> str:
        """
        This function returns a string representation of a clause.

        Returns:
            f-string that represents the clause
        """
        if not self.literals:
            return "⊥"
        return " ∨ ".join(str(l) for l in sorted(self.literals, key=lambda x: (x.name, x.negated)))