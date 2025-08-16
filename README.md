[![Python Version](https://img.shields.io/badge/python-3.12.7-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-green.svg)](LICENSE)

# 🧩 CNF SAT-Solver

A simple SAT-Solver for CNF formulas based on the **DPLL algorithm**, implemented entirely in Python using only the standard library. You can interact with it directly from the terminal with the command ```python3 run_solver.py```.

---

# ✨ Features

- 🚀 solves CNF-SAT formulas using the DPLL algorithm
- 🚀 returns a SAT/UNSAT result along with a satisfying model if one exists
- 🚀 pure Python implementation (no external dependencies)
- 🚀 command-line interface for easy usage
- 🚀 supports reading CNF formulas from standard input
- 🚀 modular design: separate classes for literals, clauses, formulas, I/O actions and solver logic

---

# 💡 Example Usage

A formula must be given to the program one clause after another.

Clauses are represented by different letters seperated by whitespaces. After each clause you must press enter.

Here a comprehensive example for the CNF formula (A ∨ B ∨ C) ∧ (¬A) ∧ (¬B ∨ D).

- ✅ start with the clause (A ∨ B ∨ C) by typing ```A B C```
- ✅ afterwards, you can insert the clause (¬A) by typing ```-A```
- ✅ finally the clause (¬B ∨ D) is represented by ```-B D```
- ✅ after typing all clauses, just press enter and give an empty line to the program

Now the solver will check your CNF for satisfiability.

The output for this example should look like this:

```
Formula: (A ∨ B ∨ C) ∧ (¬A) ∧ (¬B ∨ D) 

The formula is satisfiable (SAT).

Variable Assignment:
  A = False
  C = True
  D = True

If variables that you typed in are not in the variable assignment, then the satisfiability of the formula is independent from their truth values.
```

---

# 📂 Folder Structure
```
cnf-sat-solver/
    ├── run_solver.py
    ├── LICENSE
    ├── README.md
    ├── solver/             
        ├── __init__.py
        ├── clauses.py      # class for clauses
        ├── formula.py      # class for formulas
        ├── io.py           # I/O actions in the terminal
        ├── literals.py     # class for literals
        └── solver.py       # DPLL algorithm
```


# 📜 License

This project is licensed by the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007.