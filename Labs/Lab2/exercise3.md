# Exercise 3 — New Clue Scenario

## Code

```python
from logic import *

alice = Symbol("AliceSuspect")
bob = Symbol("BobSuspect")
carol = Symbol("CarolSuspect")

office = Symbol("office")
garage = Symbol("garage")
basement = Symbol("basement")

poison = Symbol("poison")
rope = Symbol("rope")
candlestick = Symbol("candlestick")

symbols = [alice, bob, carol, office, garage, basement, poison, rope, candlestick]

knowledge = And(
    # Layer 1: At least one suspect, room, and weapon
    Or(alice, bob, carol),
    Or(office, garage, basement),
    Or(poison, rope, candlestick)
)

# Layer 2: Cards in your hand
knowledge.add(And(
    Not(alice),
    Not(office),
    Not(poison)
))

# Layer 3: Opponent showed one of these cards
knowledge.add(Or(
    Not(bob),
    Not(garage),
    Not(rope)
))

# Layer 4: Additional facts
knowledge.add(Not(candlestick))
knowledge.add(Not(basement))

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}: YES")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

check_knowledge(knowledge)
```

## Output

```
CarolSuspect: YES
garage: YES
rope: YES
```

## Explanation

From the clues, `AliceSuspect` is false, so among the suspects only Bob or Carol remain.  
The opponent clue says at least one of `Not(BobSuspect)`, `Not(garage)`, or `Not(rope)` must be true.

We also know:
- `Not(office)`
- `Not(basement)`

So the only possible room is `garage`, which means `garage: YES`.

Since the opponent clue includes `Not(garage)` and `garage` is definitely true, `Not(garage)` is false.  
We also know:
- `Not(poison)`
- `Not(candlestick)`

So the only possible weapon is `rope`, which means `rope: YES`.

Now in the opponent clue:
- `Not(garage)` is false
- `Not(rope)` is false

So `Not(BobSuspect)` must be true, which means Bob is not the suspect.  
Since Alice is also not the suspect, the only remaining suspect is `CarolSuspect`, so `CarolSuspect: YES`.

Implicitly NO:
- AliceSuspect
- BobSuspect
- office
- basement
- poison
- candlestick

There are no MAYBE results in this case because the clues determine exactly one suspect, one room, and one weapon.
