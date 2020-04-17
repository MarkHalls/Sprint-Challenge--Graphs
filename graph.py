from util import Stack, Queue


def inverse_direction(direction):
    if direction is "n":
        return "s"
    if direction is "s":
        return "n"
    if direction is "e":
        return "w"
    if direction is "w":
        return "e"


class Graph:
    def __init__(self, world):
        self.vertices = {}
        self.world = world

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = {"n": "?", "s": "?", "w": "?", "e": "?"}

    def add_edge(self, v1, v2, direction):
        invert_direction = inverse_direction(direction)
        if v2 not in self.vertices:
            self.add_vertex(v2)
        if v1 in self.vertices and v2 in self.vertices:
            if v2 not in self.vertices[v1]:
                # create a bidirectional link
                self.vertices[v1][direction] = v2
                self.vertices[v2][invert_direction] = v1

    def get_neighbors(self, vertex_id):
        if vertex_id in self.vertices:
            vertex_room = self.world.rooms[vertex_id]
            exits = vertex_room.get_exits()
            for e in exits:
                new_room = vertex_room.get_room_in_direction(e)
                self.add_edge(vertex_id, new_room.id, e)
            return self.vertices[vertex_id]
        else:
            return None

    def dft(self, starting_vertex, prev_unvisited=None, visited=None, path=None):
        if prev_unvisited is None:
            prev_unvisited = 0
        if visited is None:
            visited = set()
        if path is None:
            path = []

        visited.add(starting_vertex)
        path.append(starting_vertex)
        neighbors = self.get_neighbors(starting_vertex)

        # count unvisited neighbors
        count = 0
        room_to_visit = []
        for _, room in neighbors.items():
            if room not in visited and room is not "?":
                count += 1
                room_to_visit.append(room)

        for room in room_to_visit:
            path = self.dft(room, starting_vertex, visited, path)
        return path + self.bfs(starting_vertex, prev_unvisited)

    def bfs(self, starting_vertex, destination_vertex):
        qq = Queue()
        qq.enqueue([starting_vertex])

        visited = set()

        while qq.size() > 0:
            path = qq.dequeue()
            if path[-1] not in visited:
                if path[-1] is destination_vertex:
                    # remove the first item since we started here
                    return path[1:]
                    # return path
                visited.add(path[-1])

                for _, next_room in self.get_neighbors(path[-1]).items():
                    if next_room is not "?":
                        new_path = list(path)
                        new_path.append(next_room)
                        qq.enqueue(new_path)

    def node_to_steps(self, node_list):
        steps = []
        for i in range(0, len(node_list)):
            try:
                current_room = node_list[i]
                next_room = node_list[i + 1]
                if current_room is not next_room:
                    for direction, room in self.vertices[current_room].items():
                        if room is next_room:
                            steps.append(direction)
            except:
                return steps
        return steps
