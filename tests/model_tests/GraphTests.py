import unittest
from setup_imports import setup_imports
setup_imports()

from model.Graph import Graph

class GraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph(adjacency_list={
            1: [2, 3],
            2: [1, 3],
            3: [1, 2],
            4: []
        })
    def test_init(self):
        self.assertIsInstance(self.graph, Graph)
    
    def test_add_directed_edge(self):
        self.graph.add_directed_edge(1, 4)
        self.assertTrue(4 in self.graph.adjacency_list[1])
        self.assertFalse(1 in self.graph.adjacency_list[4])
    
    def test_add_undirected_edge(self):
        self.graph.add_undirected_edge(1, 4)
        self.assertTrue(4 in self.graph.adjacency_list[1])
        self.assertTrue(1 in self.graph.adjacency_list[4])

    def test_check_edge(self):
        self.assertTrue(self.graph.check_edge(1, 2))
        self.assertFalse(self.graph.check_edge(3, 4))
    
    def test_get_vertices(self):
        self.assertEqual(sorted(self.graph.get_vertices()), [1, 2, 3, 4])
    
    def test_get_neighbours(self):
        self.assertEqual(sorted(self.graph.get_neighbours(1)), [2, 3])
    
    def test_get_vertex_degree(self):
        self.assertEqual(self.graph.get_vertex_degree(1), 2)
    
    def test_get_vertices_degrees(self):
        arr = self.graph.get_vertices_degrees()
        self.assertEqual(len(arr), 4)
        self.assertEqual(list(map(lambda key: key[1], arr)), [2, 2, 2, 0])
    
    def test_valid_colouring(self):
        self.assertTrue(self.graph.valid_colouring(colour_map= {1: 1, 2: 2, 3: 3, 4: 1}))
        self.assertFalse(self.graph.valid_colouring(colour_map={1: 1, 2: 1, 3: 1, 4: 1}))
        self.assertFalse(self.graph.valid_colouring(colour_map={1: 1, 2: 2, 3: 3, 4: 0}))

