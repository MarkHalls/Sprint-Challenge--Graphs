from room import Room
from player import Player
from world import World
from graph import Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
############################################
"""
Start with dft to find all rooms, then use a bfs to find the shortest path back
to the room with the next unvisited door
Repeat until all doors have been visited

What does our graph look like. 
{room_id: {n: "?", s: "?", e: "?", w: "?"}, ...}

When we visit a room we should get all connected rooms and add the return door
to our graph. 

depth first: 
append 0 -> 1 -> 12 -> 13 -> 14
BFS to find return path to nearest unvisited door
append path 14 -> 1 since 1 has unvisited doors
continue DFT
append 1 -> 2
BFS
append 2 -> 1 since we still have unvisited doors
continue DFT
append 1 -> 15 -> 16 -> 17
BFS
"""
new_graph = Graph(world)
new_graph.add_vertex(world.starting_room.id)
nodes = new_graph.dft(world.starting_room.id)
steps = new_graph.node_to_steps(nodes)
traversal_path = steps

############################################

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
