# AI Lab2 — Knowledge Representation

## Exercise 1
Truth table shows the expression is always true (tautology).

## Exercise 2
After adding Snape, the knowledge base becomes inconsistent because more than one character is true while the rule requires exactly one.

## Exercise 3
The system concludes:
- CarolSuspect = YES
- garage = YES
- rope = YES

All others are eliminated.

## Exercise 4
The added clue states that all guessed positions are wrong. This helps reduce possibilities and supports the final solution.

## Exercise 5
1. puzzle.py: 16 symbols → 2^16 = 65,536 rows  
2. mastermind.py: 16 symbols → 65,536 rows  
3. 6 colors & 6 positions: 36 symbols → 2^36 ≈ 68 billion  
4. Use SAT solvers (DPLL) to avoid checking all possibilities.
