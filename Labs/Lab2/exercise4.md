# Exercise 4 — Add a Third Clue to mastermind.py

## Code

```python
from logic import *

colors = ["red", "blue", "green", "yellow"]
symbols = []

for color in colors:
    for i in range(4):
        symbols.append(Symbol(f"{color}{i}"))

knowledge = And()

# Rule A: Every color appears in at least one position
for color in colors:
    knowledge.add(Or(
        Symbol(f"{color}0"),
        Symbol(f"{color}1"),
        Symbol(f"{color}2"),
        Symbol(f"{color}3")
    ))

# Rule B: Each color appears in exactly one position
for color in colors:
    for i in range(4):
        for j in range(4):
            if i != j:
                knowledge.add(Implication(
                    Symbol(f"{color}{i}"),
                    Not(Symbol(f"{color}{j}"))
                ))

# Rule C: Each position holds exactly one color
for i in range(4):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication(
                    Symbol(f"{c1}{i}"),
                    Not(Symbol(f"{c2}{i}"))
                ))

# Feedback 1: Exactly 2 of [red0, blue1, green2, yellow3] are correct
knowledge.add(Or(
    And(Symbol("red0"), Symbol("blue1"), Not(Symbol("green2")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("green2"), Not(Symbol("blue1")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("yellow3"), Not(Symbol("blue1")), Not(Symbol("green2"))),
    And(Symbol("blue1"), Symbol("green2"), Not(Symbol("red0")), Not(Symbol("yellow3"))),
    And(Symbol("blue1"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("green2"))),
    And(Symbol("green2"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("blue1")))
))

# Feedback 2: None of these placements are correct
knowledge.add(And(
    Not(Symbol("blue0")),
    Not(Symbol("red1")),
    Not(Symbol("green2")),
    Not(Symbol("yellow3"))
))

# Feedback 3: None of these placements are correct
knowledge.add(And(
    Not(Symbol("blue0")),
    Not(Symbol("green1")),
    Not(Symbol("red2")),
    Not(Symbol("yellow3"))
))

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
red0: YES
blue1: YES
yellow2: YES
green3: YES
```

## Explanation

Yes, the third clue completely solves the puzzle.

From Feedback 2, we know:
- `blue0` is false
- `red1` is false
- `green2` is false
- `yellow3` is false

From Feedback 3, we also know:
- `blue0` is false
- `green1` is false
- `red2` is false
- `yellow3` is false

Now go back to Feedback 1, which says exactly 2 of these are correct:
- `red0`
- `blue1`
- `green2`
- `yellow3`

But Feedback 2 already proves that:
- `green2` is false
- `yellow3` is false

So the only way Feedback 1 can still have exactly 2 correct positions is:
- `red0` = true
- `blue1` = true

Now positions 0 and 1 are fixed:
- Position 0 = red
- Position 1 = blue

The remaining colors are green and yellow for positions 2 and 3.

But Feedback 2 says `green2` is false, so green cannot be in position 2.
Therefore:
- `green3` = true
- `yellow2` = true

So the full solution is:
- Position 0 = red
- Position 1 = blue
- Position 2 = yellow
- Position 3 = green

This means the puzzle is fully solved, and there are no MAYBE results left.
