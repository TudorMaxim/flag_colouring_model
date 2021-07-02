from typing import List
from model.Graph import Graph
from algorithms.AbstractColouringAlgorithm import AbstractColouringAlgorithm


class EvolutionaryAlgorithm(AbstractColouringAlgorithm):
    def __init__(self, graph: Graph) -> None:
        super().__init__(graph)
    
    def run(self, colours_set: List) -> dict:
        # TODO: implement evolutionaty algorithm for graph colouring
        return {}
