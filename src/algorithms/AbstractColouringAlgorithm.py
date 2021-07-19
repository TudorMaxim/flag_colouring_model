import abc
from typing import List
from model.Graph import Graph


class AbstractColouringAlgorithm(metaclass=abc.ABCMeta):
    def __init__(self, graph: Graph, courses_map: dict = None) -> None:
        self._graph = graph
        self.courses_map = courses_map
    
    @abc.abstractmethod
    def run(self, colours_set: List) -> dict:
        pass
