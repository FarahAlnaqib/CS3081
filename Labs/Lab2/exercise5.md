## Exercise 5 — Scalability Analysis

1. `puzzle.py` uses 16 symbols, so `model_check` explores `2^16 = 65,536` rows.  
2. `mastermind.py` also uses 16 symbols, so it explores `2^16 = 65,536` rows.  
3. With 6 colors and 6 positions, there would be 36 symbols and `2^36 = 68,719,476,736` rows.  
4. A better approach is to use SAT solvers such as DPLL, which use unit propagation and backtracking instead of checking all possible truth assignments.
