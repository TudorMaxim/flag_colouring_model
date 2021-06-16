from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from model.Graph import Graph
from utils.Conflicts import Conflicts
from datetime import datetime


def valid_colouring(colour_map, course, graph):
    for neighbour in graph.get_neighbours(course):
        if colour_map[course] == colour_map[neighbour]:
            return False
    return True


def largest_degree_ordering(graph):
    degrees_queue = graph.get_vertices_degrees()
    colours_set = [i for i in range(1, 56)]
    max_colour = -1
    used_colours = []
    colours_map = {}
    for (course, degree) in degrees_queue:
        colours_map[course] = 0
    
    while len(degrees_queue) > 0:
        (course, _) = degrees_queue.pop(0)
        
        # Try colouring with an already used colour
        for colour in used_colours:
            colours_map[course] = colour
            if valid_colouring(colours_map, course, graph):
                break
            colours_map[course] = 0 # Try next colour
        
        # If no existent colour can be used, then add a new one
        if colours_map[course] == 0:
            max_colour += 1
            used_colours.append(colours_set[max_colour])
            colours_map[course] = used_colours[-1]
    
    return colours_map
        

if __name__ == '__main__':
    students = Student.from_json()
    teachers = Teacher.from_json()
    courses = Course.build_ids_map(Course.from_json())
    conflict_graph = Conflicts.build_graph(students, teachers)
    
    print("CONFLICT GRAPH:")
    print(conflict_graph.adjacency_list)

    start_time = datetime.now()
    colouring = largest_degree_ordering(conflict_graph)
    elapsed = datetime.now() - start_time

    print("\nTIMETABLE:")
    for course in colouring:
        print(f'{course}: Colour#{colouring[course]}')

    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
