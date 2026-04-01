# ============================================================
# CS3081 - Artificial Intelligence
# Assignment 2 - Part 2: Knowledge
# Name: _______________________
# Student ID: _________________
# ============================================================
#
# INSTRUCTIONS:
#   Read all the comments carefully.
#   Find every line that says  # TODO  and complete it.
#   Do NOT change any other lines.
#   Run the file and take a screenshot of the output.
# ============================================================

from logic import Symbol, Not, And, Or, Implication, KB, check_all

# ============================================================
# THE MYSTERY (same story, new twist)
# ============================================================
# A laptop went missing from the CS lab at Effat University.
# Three suspects: Sara, Lina, Nora
#
# The clues:
#   Clue 1: If Lina has a key  -->  Lina is guilty.
#   Clue 2: Sara does NOT have a key.
#   Clue 3: Lina was seen near the lab.
#   Clue 4: If Lina was seen near the lab  -->  Lina has a key.
#   Clue 5 (NEW): Nora has an alibi (she was NOT near the lab).
#   Clue 6 (NEW): If someone has NO alibi  -->  they are suspicious.
#
# ============================================================


# ============================================================
# SYMBOLS ALREADY DEFINED FOR YOU  (do not change)
# ============================================================

sara_key    = Symbol("SaraHasKey")
lina_key    = Symbol("LinaHasKey")
lina_seen   = Symbol("LinaSeenNearLab")
lina_guilty = Symbol("LinaIsGuilty")
nora_alibi  = Symbol("NoraHasAlibi")

# ----------------------------------------------------------
# TODO 1: Define one missing symbol.
# We need a symbol for "Nora is suspicious".
# Copy the pattern above and name it:  nora_suspicious
# The symbol name string should be:   "NoraIsSuspicious"
# ----------------------------------------------------------
# YOUR LINE HERE:
nora_suspicious = Symbol("NoraIsSuspicious")


# ----------------------------------------------------------
# All symbol NAMES for model checking
# TODO 2: Add "NoraIsSuspicious" to the list below.
# ----------------------------------------------------------
all_symbols = [
    "SaraHasKey",
    "LinaHasKey",
    "LinaSeenNearLab",
    "LinaIsGuilty",
    "NoraHasAlibi",
    "NoraIsSuspicious",
]


# ============================================================
# KNOWLEDGE BASE
# ============================================================

kb = KB()

# --- Clues 1-4 already added for you (do not change) ---
kb.tell(Implication(lina_key, lina_guilty))
kb.tell(Not(sara_key))
kb.tell(lina_seen)
kb.tell(Implication(lina_seen, lina_key))

# ----------------------------------------------------------
# TODO 3: Add Clue 5.
# Clue 5 says: "Nora HAS an alibi."  (this is a known fact)
# Hint: To say something is a known fact, just tell the KB the symbol directly.
# Example from the lab:  kb.tell(lina_seen)
# ----------------------------------------------------------
# YOUR LINE HERE:
kb.tell(nora_alibi)


# ----------------------------------------------------------
# TODO 4: Add Clue 6.
# Clue 6 says: "If Nora does NOT have an alibi  -->  Nora is suspicious."
# Hint: Use  Implication( Not(...) , ... )
# ----------------------------------------------------------
# YOUR LINE HERE:
kb.tell(Implication(Not(nora_alibi), nora_suspicious))


# ============================================================
# QUERIES  (do not change)
# ============================================================

print("=" * 52)
print("  CS3081 Assignment 2 - Knowledge Base Detective")
print("=" * 52)

# Query 1: Is Lina guilty?
answer1 = check_all(kb, lina_guilty, all_symbols)
print(f"\n Query 1 : Is Lina guilty?")
print(f"   Answer: {'YES - KB entails Lina is guilty.' if answer1 else 'NO  - KB does not entail Lina is guilty.'}")

# Query 2: Is Nora suspicious?
# This will only work once you complete TODO 1 and TODO 4
try:
    answer2 = check_all(kb, nora_suspicious, all_symbols)
    print(f"\n Query 2 : Is Nora suspicious?")
    print(f"   Answer: {'YES - KB entails Nora is suspicious.' if answer2 else 'NO  - KB does not entail Nora is suspicious.'}")
except NameError:
    print(f"\n Query 2 : Is Nora suspicious?")
    print(f"   --> Please complete TODO 1 first!")

# Query 3: Does Sara have a key?
answer3 = check_all(kb, sara_key, all_symbols)
print(f"\n Query 3 : Does Sara have a key?")
print(f"   Answer: {'YES - KB entails Sara has a key.' if answer3 else 'NO  - KB does not entail Sara has a key.'}")

print("\n" + "=" * 52)