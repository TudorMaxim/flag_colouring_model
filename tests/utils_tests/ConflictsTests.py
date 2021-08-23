import unittest
from setup_imports import setup_imports
setup_imports()

from utils.Conflicts import Conflicts
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course

class ConflictsTests(unittest.TestCase):

    def setUp(self) -> None:
        dataset = './tests/mock_data.json'
        self.students = Student.from_json(dataset)
        self.teachers = Teacher.from_json(dataset)
        self.courses = Course.from_json(dataset)
        self.conflict_graph = Conflicts.build_graph(list(self.students), list(self.teachers))
        
    def test_edge_beween_two_courses_of_a_student(self):
        for student in self.students:
            for i in range(len(student.course_ids)):
                for j in range(len(student.course_ids)):
                    if i == j: 
                        continue
                    self.assertTrue(self.conflict_graph.check_edge(student.course_ids[i], student.course_ids[j]))
    
    def test_edge_between_two_courses_of_a_teacher(self):
        for teacher in self.teachers:
            for i in range(len(teacher.course_ids)):
                for j in range(len(teacher.course_ids)):
                    if i == j:
                        continue
                    self.assertTrue(self.conflict_graph.check_edge(teacher.course_ids[i], teacher.course_ids[j]))

