from typing import Any, List


class Graph:
    def __init__(self, adjacency_list=None):
        if adjacency_list is None:
            adjacency_list = {}
        self.adjacency_list = adjacency_list
    
    def add_directed_edge(self, x, y):
        if x not in self.adjacency_list:
            self.adjacency_list[x] = [y]
        else:
            self.adjacency_list[x].append(y)
    
    def add_undirected_edge(self, x, y):
        self.add_directed_edge(x, y)
        self.add_directed_edge(y, x)

    def check_edge(self, x, y) -> bool:
        if x not in self.adjacency_list:
            return False
        return y in self.adjacency_list[x]
    
    def get_vertices(self) -> List:
        return [*self.adjacency_list]

    def get_neighbours(self, vertex) -> List:
        if vertex not in self.adjacency_list:
            return []
        return self.adjacency_list[vertex]
    
    def get_vertex_degree(self, vertex) -> int:
        if vertex not in self.adjacency_list:
            return 0
        return len(self.adjacency_list[vertex])

    def get_vertices_degrees(self) -> List:
        degrees = [(vertex, self.get_vertex_degree(vertex)) for vertex in self.get_vertices()]
        return sorted(degrees, key=lambda x: x[1], reverse=True)

    def valid_colouring_for(self, vertex: Any, colour_map: dict) -> bool:
        for neighbour in self.get_neighbours(vertex):
            if colour_map[vertex] == colour_map[neighbour]:
                return False
        return True

    def valid_colouring(self, colour_map: dict) -> bool:
        for vertex in self.get_vertices():
            if vertex not in colour_map or colour_map[vertex] == 0: # Uncoloured vertex
                return False
            if not self.valid_colouring_for(vertex, colour_map): # 2 adjacent vertices having the same colour
                return False
        return True

    def density(self) -> float:
        vertices = self.get_vertices()
        vertices_cnt = len(vertices)
        denominator = vertices_cnt * (vertices_cnt - 1) / 2
        numerator = 0
        for i in range(vertices_cnt):
            for j in range(i + 1, vertices_cnt):
                numerator += 1 if self.check_edge(vertices[i], vertices[j]) else 0
        return numerator / denominator
    
