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

    def check_edge(self, x, y):
        if x not in self.adjacency_list:
            return False
        return y in self.adjacency_list[x]
    
    def get_vertices(self):
        return [*self.adjacency_list]

    def get_neighbours(self, vertex):
        if vertex not in self.adjacency_list:
            return []
        return self.adjacency_list[vertex]
    
    def get_vertex_degree(self, vertex):
        if vertex not in self.adjacency_list:
            return 0
        return len(self.adjacency_list[vertex])
