# Exercise 1 — Truth Table

Expression:
(P ∧ Q) → (P ∨ ¬Q)

| P | Q | P ∧ Q | P ∨ ¬Q | Result |
|---|---|-------|--------|--------|
| T | T | T | T | T |
| T | F | F | T | T |
| F | T | F | F | T |
| F | F | F | T | T |

## Explanation
The expression is always true for all values of P and Q, so it is a tautology.


## Verification using model_check()

```python
from logic import *

P = Symbol("P")
Q = Symbol("Q")

sentence = Implication(And(P, Q), Or(P, Not(Q)))

models = [
    {"P": True, "Q": True},
    {"P": True, "Q": False},
    {"P": False, "Q": True},
    {"P": False, "Q": False}
]

for model in models:
    print(model, "->", sentence.evaluate(model))





