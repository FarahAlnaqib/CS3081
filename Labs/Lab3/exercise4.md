# Exercise 4 – Remove a Clue

## (a) Is Lina still guilty according to the KB?

No, Lina is no longer proven guilty.

Output:
NO – The KB does NOT entail that Lina is guilty.

---

## (b) What changed?

The clue stating that Lina was seen near the room was removed from the knowledge base.

Previously, this clue allowed the system to infer that Lina had a key, and then conclude that she was guilty.

After removing it, the system can no longer prove that Lina has a key, so it also cannot prove that she is guilty.

---

## (c) Why did removing one clue change the result?

The knowledge base depends on connected logical rules.

Before:
- Lina was seen near the room
- If Lina was seen near the room, then she has a key
- If Lina has a key, then she is guilty

After removing the first fact, the chain is broken. Because of that, the final conclusion can no longer be reached.
## Output Screenshot

![Exercise 4 Output](images/exercise4_output.png)
