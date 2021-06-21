import numpy as np
from typing import List
from model.Graph import Graph
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from utils.Conflicts import Conflicts
from datetime import datetime


def get_common_neighbours(v: int, graph: Graph, vertices_set: List) -> List:
    neighbours = graph.get_neighbours(v)
    return np.intersect1d(np.array(vertices_set), np.array(neighbours)).tolist()


def select_vertex(graph: Graph, candidates: List, noncandidates: List) -> int:
    selected = candidates[0]
    max_common_neighbours = 0
    min_candidate_neighbours = 1e5
    for vertex in candidates:
        common_neighbours = get_common_neighbours(vertex, graph, noncandidates)
        common_neighbours_cnt = len(common_neighbours)
        candidate_neighbours = get_common_neighbours(vertex, graph, candidates)
        candidate_neighbours_cnt = len(candidate_neighbours)
        if common_neighbours_cnt > max_common_neighbours or \
            (common_neighbours_cnt == max_common_neighbours and candidate_neighbours_cnt < min_candidate_neighbours):
            max_common_neighbours = common_neighbours_cnt
            min_candidate_neighbours = candidate_neighbours_cnt
            selected = vertex
    return selected


def expand(v0: int, graph: Graph, candidates: List, colour_map: dict, colour_set: List, active_colour: int):
    noncandidates = graph.get_neighbours(v0)
    candidates = np.setdiff1d(np.array(candidates), np.array(noncandidates)).tolist()
    while candidates:
        v = select_vertex(graph, candidates, noncandidates)
        colour_map[v] = colour_set[active_colour]
        neighbours = get_common_neighbours(v, graph, candidates)
        noncandidates = np.union1d(np.array(noncandidates), np.array(neighbours)).tolist()
        candidates = np.setdiff1d(np.array(candidates), np.array([v]))
        candidates = np.setdiff1d(candidates, np.array(neighbours)).tolist()


def recursive_largest_first_algorithm(graph: Graph) -> dict:
    colour_set = [i for i in range(1, 61)]
    active_colour = 0
    colour_map = {}
    candidates = list(map(lambda x: x[0], graph.get_vertices_degrees()))
    while candidates:
        course = candidates.pop(0)
        colour_map[course] = colour_set[active_colour]
        expand(course, graph, candidates, colour_map, colour_set, active_colour)
        candidates = list(map(lambda x: x[0], graph.get_vertices_degrees()))
        candidates = list(filter(lambda x: x not in colour_map, candidates))
        active_colour += 1
    return colour_map
        
       
if __name__ == '__main__':
    students = Student.from_json()
    teachers = Teacher.from_json()
    courses = Course.build_ids_map(Course.from_json())
    conflict_graph = Conflicts.build_graph(students, teachers)
    
    print("CONFLICT GRAPH:")
    print(conflict_graph.adjacency_list)

    start_time = datetime.now()
    colouring = recursive_largest_first_algorithm(conflict_graph)
    elapsed = datetime.now() - start_time

    print("\nTIMETABLE:")
    for course in colouring:
        print(f'{course}: Colour#{colouring[course]}')

    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
