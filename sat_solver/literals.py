from dataclasses import dataclass
from typing import Dict, Optional



@dataclass(frozen=True)
class Literal:
    """
    This class represents a propositional literal.
    
    Args:
        name (str): name of literal
        negated (bool): boolean that indicates weather the literal is negated or not
    """
    name: str
    negated: bool = False



    def eval(self, assignment: Dict[str, bool]) -> Optional[bool]:
        """
        This function evaluates a literal under an assignment.

        Args:
            assignment (Dict[str, bool]): variable assignment
        
        Returns:
            Optional[bool]: truth value of literal or None if variable is unassigned
        """
        if self.name not in assignment:
            return None
        val = assignment[self.name]
        return (not val) if self.negated else val



    def __str__(self) -> str:
        """
        This function produces a string representation of a Literal.

        Returns:
            f-string of variable name with optional negation sign (¬)
        """
        return f"¬{self.name}" if self.negated else self.name