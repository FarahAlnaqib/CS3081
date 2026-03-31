
# CS3081 – Artificial Intelligence  
## Lab 3: Search & Knowledge

---

## 📌 Overview
This lab covers two main AI concepts:
- **Search (BFS):** Finding the shortest path between cities
- **Knowledge (Logic):** Using a Knowledge Base to infer conclusions

---

## 🧠 Part 1 – BFS Search

Implemented Breadth-First Search (BFS) to find the shortest path.

**Key Points:**
- Uses a queue (FIFO)
- Explores level by level
- Guarantees shortest path

**Exercises:**
- Changed goal to *Madinah*
- Added new city *Abha*

**Example Path:**

Makkah → Taif → Abha

---

## 🧠 Part 2 – Knowledge Base

Built a logical AI agent using propositional logic.

**Key Concepts:**
- Symbols represent facts
- Rules connect facts using implication
- Model checking tests all possibilities

**Exercises:**
- Added clue: Nora has a key
- Removed clue: Lina seen near room

**Results:**
- Lina is **not proven guilty** after removing the clue
- Nora is **not proven guilty** due to missing rule

---

## 📁 Files Included
- `part1_search.py`
- `part2_knowledge.py`
- `discussion.pdf`
- Screenshots for all exercises

---

## 👩‍💻 Author
Name: Farah Alnaqib 
Student ID: S22107915 

---

## 🎯 Summary
This lab demonstrates:
- How BFS finds shortest paths
- How logic can be used for reasoning in AI
