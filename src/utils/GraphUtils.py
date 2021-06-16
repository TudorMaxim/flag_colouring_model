from model.Course import Course
from model.Graph import Graph


class GraphUtils:
    @staticmethod
    def valid_colouring(course: Course, graph: Graph, colour_map: dict) -> bool:
        for neighbour in graph.get_neighbours(course):
            if colour_map[course] == colour_map[neighbour]:
                return False
        return True
