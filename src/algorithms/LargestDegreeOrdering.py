from typing import List
from model.Course import Course
from model.Graph import Graph
from algorithms.AbstractColouringAlgorithm import AbstractColouringAlgorithm
from model.Student import Student
from model.Teacher import Teacher


class LargestDegreeOrdering(AbstractColouringAlgorithm):
    def __init__(
        self,
        graph: Graph,
        students_map: dict[int, Student] = None,
        teachers_map: dict[int, Teacher] = None,
        courses_map: dict[int, Course] = None
    ) -> None:
        super().__init__(graph, students_map, teachers_map, courses_map)
    
    def run(self, colours_set: List) -> dict:
        queue = self._graph.get_vertices_degrees()
        max_colour = -1
        used_colours = []
        colours_map = {}
        for (course, _) in queue:
            colours_map[course] = 0
        while queue:
            (course, _) = queue.pop(0)
            # Try colouring with an already used colour
            for colour in used_colours:
                colours_map[course] = colour
                if self._graph.valid_colouring_for(course, colours_map):
                    break
                colours_map[course] = 0  # Try next colour
            # If no existent colour can be used, then add a new one
            if colours_map[course] == 0:
                max_colour += 1
                used_colours.append(colours_set[max_colour])
                colours_map[course] = used_colours[-1]
        return colours_map
