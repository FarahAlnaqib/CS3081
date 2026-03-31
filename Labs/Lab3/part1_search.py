# ============================================================
# CS3081 - Artificial Intelligence
# Lab 2 - Part 1: Search
# Name: _______________________
# Student ID: _________________
# ============================================================

# We represent a map as a dictionary.
# Each city points to a list of cities it is directly connected to.

city_map = {
    "Makkah": ["Jeddah", "Taif"],
    "Jeddah": ["Makkah", "Riyadh", "Madinah"],
    "Taif": ["Makkah", "Riyadh", "Abha"],
    "Riyadh": ["Jeddah", "Taif", "Dammam"],
    "Madinah": ["Jeddah"],
    "Dammam": ["Riyadh"],
    "Abha": ["Taif"]
}

# ============================================================
# STEP 1: Understand the Node
# A Node stores:
#   - city      : where we are now
#   - parent    : which node led us here
# ============================================================

class Node:
    def __init__(self, city, parent=None):
        self.city = city
        self.parent = parent

    def path(self):
        """Trace back from this node to the start and return the full path."""
        route = []
        current = self
        while current is not None:
            route.append(current.city)
            current = current.parent
        route.reverse()   # We traced backwards, so reverse it
        return route


# ============================================================
# STEP 2: BFS - Breadth-First Search
# We use a QUEUE (first in, first out) for the frontier.
# ============================================================

from collections import deque   # deque = double-ended queue (works as a queue)

def bfs(start, goal):
    print(f"\n🔍 Searching from '{start}' to '{goal}' using BFS...\n")

    # --- Create the starting node ---
    start_node = Node(city=start, parent=None)

    # --- The frontier holds nodes we want to explore ---
    frontier = deque()
    frontier.append(start_node)

    # --- The explored set prevents visiting the same city twice ---
    explored = set()

    step = 1   # Just for printing

    # --- Main BFS loop ---
    while frontier:

        # Take the FIRST node from the queue (FIFO)
        current_node = frontier.popleft()
        current_city = current_node.city

        print(f"  Step {step}: Visiting '{current_city}'")
        step += 1

        # --- Did we reach the goal? ---
        if current_city == goal:
            print(f"\n✅ Goal reached! '{goal}' found.")
            return current_node.path()

        # --- Mark this city as explored ---
        explored.add(current_city)

        # --- Add neighbors to the frontier ---
        for neighbor in city_map[current_city]:
            if neighbor not in explored:
                neighbor_node = Node(city=neighbor, parent=current_node)
                frontier.append(neighbor_node)
                explored.add(neighbor)   # Mark when added, not when visited

    # If we exit the loop without finding the goal
    print("❌ No path found.")
    return None


# ============================================================
# STEP 3: Run the search
# ============================================================

if __name__ == "__main__":

    start_city = "Makkah"
    goal_city  = "Abha"

    result = bfs(start_city, goal_city)

    if result:
        print(f"\n📍 Path found ({len(result)-1} steps):")
        print(" → ".join(result))
    else:
        print("\nNo path exists between the two cities.")
