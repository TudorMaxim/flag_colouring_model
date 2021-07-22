import abc
from typing import List
from model.Graph import Graph
from model.Student import Student
from model.Teacher import Teacher


class AbstractColouringAlgorithm(metaclass=abc.ABCMeta):
    def __init__(
        self, 
        graph: Graph,
        students_map: dict[int, Student] = None,
        teachers_map: dict[int, Teacher] = None,
        courses_map: dict[int, Teacher] = None
    ) -> None:
        self._graph = graph
        self.students_map = students_map
        self.teachers_map = teachers_map
        self.courses_map = courses_map
    
    @abc.abstractmethod
    def run(self, colours_set: List) -> dict:
        pass
