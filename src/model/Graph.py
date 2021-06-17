from typing import Any, List
import numpy as np


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
