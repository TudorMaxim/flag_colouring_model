from model.Graph import Graph

class Conflicts:
    @staticmethod
    def check(graph, courses):
        for i in range(len(courses) - 1):
            for j in range(i + 1, len(courses)):
                if not graph.check_edge(courses[i], courses[j]):
                    graph.add_undirected_edge(courses[i], courses[j])
        return graph
    
    @staticmethod
    def build_graph(students, teachers, courses):
        teacher_courses = Graph(adjacency_list={
            teachers[0]: [courses[0], courses[2]],
            teachers[1]: [courses[1], courses[3]]
        })
        student_courses = Graph(adjacency_list={
            students[0]: [courses[0], courses[3]],
            students[1]: [courses[0], courses[1]],
            students[2]: [courses[1], courses[3]],
            students[3]: [courses[2]],
            students[4]: [courses[0], courses[2]],
        })

        conflict_graph = Graph()
        for student in students:
            conflicting_courses = student_courses.get_neighbours(student)
            conflict_graph = Conflicts.check(conflict_graph, conflicting_courses)

        for teacher in teachers:
            conflicting_courses = teacher_courses.get_neighbours(teacher)
            conflict_graph = Conflicts.check(conflict_graph, conflicting_courses)
        
        return conflict_graph