from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from model.Graph import Graph
from utils.Conflicts import Conflicts

def largest_degree_ordering(graph):
    degrees = [graph.get_vertex_degree(vertex) for vertex in graph.get_vertices()]
    print(degrees)

if __name__ == '__main__':
    students = Student.from_json()
    teachers = Teacher.from_json()
    courses = Course.from_json()
    conflict_graph = Conflicts.build_graph(students, teachers, courses)
    for vertex in conflict_graph.adjacency_list:
        conflicts = [str(course) for course in conflict_graph.adjacency_list[vertex]]
        print(f'{str(vertex)}: {str(conflicts)}')
    