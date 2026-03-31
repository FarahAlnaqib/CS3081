# ============================================================
# CS3081 - Artificial Intelligence
# Lab 3 - Part 2: Knowledge & Propositional Logic
# Name: _______________________
# Student ID: _________________
# ============================================================

from logic import Symbol, Not, And, Or, Implication, KB, check_all

# ============================================================
# STEP 1: Define Propositional Symbols
# ============================================================

sara_key  = Symbol("SaraHasKey")
lina_key  = Symbol("LinaHasKey")
lina_seen = Symbol("LinaSeenNearRoom")
lina_guilty = Symbol("LinaIsGuilty")

nora_key = Symbol("NoraHasKey")
nora_guilty = Symbol("NoraIsGuilty")

all_symbols = [
    "SaraHasKey",
    "LinaHasKey",
    "LinaSeenNearRoom",
    "LinaIsGuilty",
    "NoraHasKey",
    "NoraIsGuilty"
]

# ============================================================
# STEP 2: Build the Knowledge Base
# ============================================================

kb = KB()

# Clue 1: If Lina has a key → Lina is guilty
kb.tell(Implication(lina_key, lina_guilty))

# Clue 2: Sara does NOT have a key
kb.tell(Not(sara_key))

# Clue 3 removed for Exercise 4
# kb.tell(lina_seen)

# Clue 4: If Lina was seen near the room → Lina has a key
kb.tell(Implication(lina_seen, lina_key))

# Exercise 3 clue
kb.tell(nora_key)

# ============================================================
# STEP 3: Ask the Knowledge Base
# ============================================================

print("=" * 50)
print("  CS3081 Lab 3 – Knowledge Base Detective")
print("=" * 50)

answer = check_all(kb, lina_guilty, all_symbols)

if answer:
    print("\n🔍 Query:  Is Lina guilty?")
    print("✅ YES  –  The KB ENTAILS that Lina is guilty.\n")
else:
    print("\n🔍 Query:  Is Lina guilty?")
    print("❌ NO   –  The KB does NOT entail that Lina is guilty.\n")

answer2 = check_all(kb, sara_key, all_symbols)

print("🔍 Query:  Does Sara have a key?")
if answer2:
    print("✅ YES  –  The KB entails Sara has a key.\n")
else:
    print("❌ NO   –  The KB does NOT entail Sara has a key.\n")

answer3 = check_all(kb, nora_guilty, all_symbols)

print("🔍 Query:  Is Nora guilty?")
if answer3:
    print("✅ YES  –  The KB entails that Nora is guilty.\n")
else:
    print("❌ NO   –  The KB does NOT entail that Nora is guilty.\n")