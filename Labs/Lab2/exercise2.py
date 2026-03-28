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
print("dumbledore:", model_check(knowledge, dumbledore))
print("snape:", model_check(knowledge, snape))
