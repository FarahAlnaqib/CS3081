# Exercise 2 — Extend harry.py

## Code

```python
from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")
snape = Symbol("snape")

knowledge = And(
    # Original rule
    Implication(Not(rain), hagrid),

    # Harry met exactly one of Hagrid, Dumbledore, or Snape
    Or(hagrid, dumbledore, snape),
    Not(And(hagrid, dumbledore)),
    Not(And(hagrid, snape)),
    Not(And(dumbledore, snape)),

    # Original fact
    dumbledore,

    # New rule
    Implication(rain, Not(snape)),

    # New fact
    snape
)

print("rain:", model_check(knowledge, rain))
print("not rain:", model_check(knowledge, Not(rain)))
print("hagrid:", model_check(knowledge, hagrid))
print("not hagrid:", model_check(knowledge, Not(hagrid)))
print("dumbledore:", model_check(knowledge, dumbledore))
print("not dumbledore:", model_check(knowledge, Not(dumbledore)))
print("snape:", model_check(knowledge, snape))
print("not snape:", model_check(knowledge, Not(snape)))
```

## Output

```
rain: True
not rain: True
hagrid: True
not hagrid: True
dumbledore: True
not dumbledore: True
snape: True
not snape: True
```

## Explanation

The knowledge base is inconsistent.

This is because the rules state that Harry met exactly one of Hagrid, Dumbledore, or Snape, but the knowledge base also includes both `dumbledore` and `snape` as true. This violates the “exactly one” constraint, creating a contradiction.

Because of this inconsistency, there is no valid model that satisfies all the rules at the same time. As a result, `model_check()` returns `True` for every statement and also for its negation.

This means the system can incorrectly prove both a statement and its opposite, which shows that the knowledge base is logically inconsistent.
