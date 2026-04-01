# ============================================================
# CS3081 - Artificial Intelligence
# Assignment 2 - Part 1: Search
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

from collections import deque

# ============================================================
# THE CITY MAP
# The map already has 6 cities.
# You will add 2 more cities below.
# ============================================================

city_map = {
    "Makkah":  ["Jeddah", "Taif"],
    "Jeddah":  ["Makkah", "Riyadh", "Madinah"],
    "Taif":    ["Makkah", "Riyadh", "Abha"],
    "Riyadh":  ["Jeddah", "Taif", "Dammam"],
    "Madinah": ["Jeddah", "Yanbu"],
    "Dammam":  ["Riyadh"],

    # ----------------------------------------------------------
    # TODO 1: Add Abha to the map.
    # Abha is connected to: Taif
    # Write it exactly like the cities above.
    # ----------------------------------------------------------
    # YOUR LINE HERE:
    "Abha": ["Taif"],

    # ----------------------------------------------------------
    # TODO 2: Add ONE city of your own choice.
    # Pick any Saudi city. Connect it to at least one city above.
    # Example:  "Yanbu": ["Madinah"]
    # ----------------------------------------------------------
    # YOUR LINE HERE:
    "Yanbu": ["Madinah"]

}

# ----------------------------------------------------------
# IMPORTANT: After adding your new cities above,
# you must also ADD them to the neighbor lists of their connected cities.
#
# Example: If you added  "Abha": ["Taif"]
# then Taif must also list Abha:
#   "Taif": ["Makkah", "Riyadh", "Abha"]   <-- add Abha here
#
# Go back to the city_map above and update the existing cities.
# ----------------------------------------------------------


# ============================================================
# NODE CLASS  (do not change)
# ============================================================

class Node:
    def __init__(self, city, parent=None):
        self.city = city
        self.parent = parent

    def path(self):
        route = []
        current = self
        while current is not None:
            route.append(current.city)
            current = current.parent
        route.reverse()
        return route


# ============================================================
# BFS FUNCTION  (do not change)
# ============================================================

def bfs(start, goal):
    print(f"\n Searching from '{start}' to '{goal}' using BFS...\n")

    start_node = Node(city=start, parent=None)
    frontier = deque()
    frontier.append(start_node)
    explored = set()
    step = 1

    while frontier:
        current_node = frontier.popleft()
        current_city = current_node.city

        print(f"  Step {step}: Visiting '{current_city}'")
        step += 1

        if current_city == goal:
            print(f"\n Goal reached! '{goal}' found.")
            return current_node.path()

        explored.add(current_city)

        for neighbor in city_map[current_city]:
            if neighbor not in explored:
                neighbor_node = Node(city=neighbor, parent=current_node)
                frontier.append(neighbor_node)
                explored.add(neighbor)

    print(" No path found.")
    return None


# ============================================================
# RUN THE SEARCH
# ============================================================

# ----------------------------------------------------------
# TODO 3: Set start_city to  "Makkah"
# ----------------------------------------------------------
start_city = "Makkah"    # already done for you

# ----------------------------------------------------------
# TODO 4: Set goal_city to your NEW city (the one you added in TODO 2).
# ----------------------------------------------------------
goal_city = "Yanbu"    # YOUR CITY NAME HERE  (keep the quotes)


# ============================================================
# MAIN  (do not change)
# ============================================================

if __name__ == "__main__":

    # Check that the student filled in the goal city
    if goal_city == "":
        print(" Please set goal_city in TODO 4 before running!")
    else:
        result = bfs(start_city, goal_city)
        if result:
            print(f"\n Path found ({len(result)-1} steps):")
            print(" -> ".join(result))
        else:
            print("\n No path exists between the two cities.")