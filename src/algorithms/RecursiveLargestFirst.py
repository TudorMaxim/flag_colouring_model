import numpy as np
from typing import List
from model.Graph import Graph
from algorithms.AbstractColouringAlgorithm import AbstractColouringAlgorithm


class RecursiveLargestFirst(AbstractColouringAlgorithm):
    def __init__(self, graph: Graph, courses_map: dict = None) -> None:
        super().__init__(graph, courses_map)

    def __get_common_neighbours(self, v: int, vertices_set: List) -> List:
        neighbours = self._graph.get_neighbours(v)
        return np.intersect1d(np.array(vertices_set), np.array(neighbours)).tolist()


    def __select_vertex(self, candidates: List, noncandidates: List) -> int:
        selected = candidates[0]
        max_common_neighbours = 0
        min_candidate_neighbours = 1e5
        for vertex in candidates:
            common_neighbours = self.__get_common_neighbours(vertex, noncandidates)
            common_neighbours_cnt = len(common_neighbours)
            candidate_neighbours = self.__get_common_neighbours(vertex, candidates)
            candidate_neighbours_cnt = len(candidate_neighbours)
            if common_neighbours_cnt > max_common_neighbours or \
                    (common_neighbours_cnt == max_common_neighbours and candidate_neighbours_cnt < min_candidate_neighbours):
                max_common_neighbours = common_neighbours_cnt
                min_candidate_neighbours = candidate_neighbours_cnt
                selected = vertex
        return selected


    def __expand(self, v0: int, candidates: List, colour_map: dict, colour_set: List, active_colour: int):
        noncandidates = self._graph.get_neighbours(v0)
        candidates = np.setdiff1d(np.array(candidates),
                                np.array(noncandidates)).tolist()
        while candidates:
            v = self.__select_vertex(candidates, noncandidates)
            colour_map[v] = colour_set[active_colour]
            neighbours = self.__get_common_neighbours(v, candidates)
            noncandidates = np.union1d(
                np.array(noncandidates), np.array(neighbours)).tolist()
            candidates = np.setdiff1d(np.array(candidates), np.array([v]))
            candidates = np.setdiff1d(candidates, np.array(neighbours)).tolist()


    def run(self, colours_set: List) -> dict:
        active_colour = 0
        colour_map = {}
        candidates = list(map(lambda x: x[0], self._graph.get_vertices_degrees()))
        while candidates:
            course = candidates.pop(0)
            colour_map[course] = colours_set[active_colour]
            self.__expand(course, candidates, colour_map, colours_set, active_colour)
            candidates = list(map(lambda x: x[0], self._graph.get_vertices_degrees()))
            candidates = list(filter(lambda x: x not in colour_map, candidates))
            active_colour += 1
        return colour_map
