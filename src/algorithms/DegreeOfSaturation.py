from typing import List
from model.Course import Course
from model.Graph import Graph
from algorithms.AbstractColouringAlgorithm import AbstractColouringAlgorithm
from model.Student import Student
from model.Teacher import Teacher


class DegreeOfSaturation(AbstractColouringAlgorithm):
    def __init__(
        self,
        graph: Graph,
        students_map: dict[int, Student] = None,
        teachers_map: dict[int, Teacher] = None,
        courses_map: dict[int, Course] = None
    ) -> None:
        super().__init__(graph, students_map, teachers_map, courses_map)

    def __saturation_degree(self, course: int, colour_map: dict) -> int:
        used_colours = []
        for vertex in self._graph.get_neighbours(course):
            if colour_map[vertex] and colour_map[vertex] not in used_colours:
                used_colours.append(colour_map[vertex])
        return len(used_colours)


    def __uncoloured_neighbours_count(self, course: int, colour_map: dict) -> int:
        degree = 0
        for vertex in self._graph.get_neighbours(course):
            degree += 1 if colour_map[vertex] == 0 else 0
        return degree


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
            queue = sorted(
                queue,
                key=lambda course: (
                    self.__saturation_degree(course, colours_map),
                    self.__uncoloured_neighbours_count(course, colours_map)
                ),
                reverse=True
            )
        return colours_map
