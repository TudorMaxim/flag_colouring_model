from model.Graph import Graph

class Conflicts:
    @staticmethod
    def check(graph, course_ids):
        for i in range(len(course_ids) - 1):
            for j in range(i + 1, len(course_ids)):
                if not graph.check_edge(course_ids[i], course_ids[j]):
                    graph.add_undirected_edge(course_ids[i], course_ids[j])
        return graph
    
    @staticmethod
    def build_graph(students, teachers):
        conflict_graph = Graph()
        for student in students:
            conflict_graph = Conflicts.check(conflict_graph, student.course_ids)

        for teacher in teachers:
            conflict_graph = Conflicts.check(conflict_graph, teacher.course_ids)
        
        return conflict_graph
