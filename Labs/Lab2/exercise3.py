import termcolor
from logic import *

# Define suspects
alice = Symbol("AliceSuspect")
bob = Symbol("BobSuspect")
carol = Symbol("CarolSuspect")
characters = [alice, bob, carol]

# Define rooms
office = Symbol("office")
garage = Symbol("garage")
basement = Symbol("basement")
rooms = [office, garage, basement]

# Define weapons
poison = Symbol("poison")
rope = Symbol("rope")
candlestick = Symbol("candlestick")
weapons = [poison, rope, candlestick]

symbols = characters + rooms + weapons


# Function to check results
def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: YES", "green")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")


# Build knowledge base
knowledge = And(
    # There must be one suspect, one room, and one weapon
    Or(alice, bob, carol),
    Or(office, garage, basement),
    Or(poison, rope, candlestick)
)

# Cards in your hand → cannot be the solution
knowledge.add(And(
    Not(alice),
    Not(office),
    Not(poison)
))

# Opponent showed one of these (we don't know which one)
knowledge.add(Or(
    Not(bob),
    Not(garage),
    Not(rope)
))

# Additional known facts
knowledge.add(Not(candlestick))
knowledge.add(Not(basement))


# Run inference
check_knowledge(knowledge)
