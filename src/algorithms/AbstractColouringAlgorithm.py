import abc
from typing import List
from model.Graph import Graph


class AbstractColouringAlgorithm(metaclass=abc.ABCMeta):
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
    
    @abc.abstractmethod
    def run(self, colours_set: List) -> dict:
        pass
