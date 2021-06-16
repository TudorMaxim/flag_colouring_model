from model.Graph import Graph
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from utils.Conflicts import Conflicts
from utils.GraphUtils import GraphUtils
from datetime import datetime


def saturation_degree(course: int, graph: Graph, colour_map: dict) -> int:
    used_colours = []
    for vertex in graph.get_neighbours(course):
        if colour_map[vertex] and colour_map[vertex] not in used_colours:
            used_colours.append(colour_map[vertex])
    return len(used_colours)


def uncoloured_neighbours_count(course: int, graph: Graph, colour_map: dict) -> int:
    degree = 0
    for vertex in graph.get_neighbours(course):
        degree += 1 if colour_map[vertex] == 0 else 0
    return degree


def degree_of_saturation_algorithm(graph: Graph) -> dict:
    queue = graph.get_vertices_degrees()
    colours_set = [i for i in range(1, 60)]
    max_colour = -1
    used_colours = []
    colours_map = {}
    for (course, _) in queue:
        colours_map[course] = 0
    
    while len(queue) > 0:
        (course, _) = queue.pop(0)
        
        # Try colouring with an already used colour
        for colour in used_colours:
            colours_map[course] = colour
            if GraphUtils.valid_colouring(course, graph, colours_map):
                break
            colours_map[course] = 0 # Try next colour
        
        # If no existent colour can be used, then add a new one
        if colours_map[course] == 0:
            max_colour += 1
            used_colours.append(colours_set[max_colour])
            colours_map[course] = used_colours[-1]

        queue = sorted(
            queue,
            key=lambda course: (
                saturation_degree(course, graph, colours_map),
                uncoloured_neighbours_count(course, graph, colours_map)
            ),
            reverse=True
        )
    return colours_map


if __name__ == '__main__':
    students = Student.from_json()
    teachers = Teacher.from_json()
    courses = Course.build_ids_map(Course.from_json())
    conflict_graph = Conflicts.build_graph(students, teachers)
    
    print("CONFLICT GRAPH:")
    print(conflict_graph.adjacency_list)

    start_time = datetime.now()
    colouring = degree_of_saturation_algorithm(conflict_graph)
    elapsed = datetime.now() - start_time

    print("\nTIMETABLE:")
    for course in colouring:
        print(f'{course}: Colour#{colouring[course]}')

    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
