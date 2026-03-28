# Exercise 5 — Scalability Analysis

## 1. puzzle.py

puzzle.py uses 16 symbols.

This is because there are 4 people and 4 houses, so:
4 × 4 = 16 symbols

The number of truth-table rows explored by model_check is:
2^16 = 65,536 rows

---

## 2. mastermind.py

mastermind.py also uses 16 symbols.

This is because there are 4 colors and 4 positions, so:
4 × 4 = 16 symbols

The number of rows explored is:
2^16 = 65,536 rows

---

## 3. Extended mastermind (6 colors, 6 positions)

If we extend the problem to 6 colors and 6 positions:

Number of symbols:
6 × 6 = 36 symbols

Number of rows:
2^36 = 68,719,476,736 rows

This is extremely large and not practical to compute.

---

## 4. Better Algorithm

A better approach is using SAT solvers, such as the DPLL algorithm.

These algorithms improve performance by avoiding checking all possible combinations.  
They use techniques like:

- **Unit propagation**: If a variable must be true to satisfy a rule, it is assigned immediately.
- **Backtracking**: The algorithm stops exploring invalid paths early and goes back to try other possibilities.

This reduces the search space significantly and avoids exploring all 2^n possibilities, making it much more efficient than truth-table enumeration.
