class Graph:
    def __init__(self, adjancy_list=None):
        if adjancy_list is None:
            adjancy_list = {}
        self.adjancy_list = adjancy_list
    
    def add_directed_edge(self, x, y):
        if x not in self.adjancy_list:
            self.adjacency_list[x] = [y]
        else:
            self.adjacency_list[x].append(y)
    
    def add_undirected_edge(self, x, y):
        self.add_directed_edge(x, y)
        self.add_directed_edge(y, x)
