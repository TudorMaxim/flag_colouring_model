import unittest
from setup_imports import setup_imports
setup_imports()

from utils.Conflicts import Conflicts
from model.Factory import Factory
from model.EntityType import EntityType


class ConflictsTests(unittest.TestCase):

    def setUp(self) -> None:
        dataset = './tests/mock_data.json'
        self.students = Factory.from_json(entity_type=EntityType.STUDENT, path=dataset)
        self.teachers = Factory.from_json(entity_type=EntityType.TEACHER, path=dataset)
        self.courses = Factory.from_json(entity_type=EntityType.COURSE, path=dataset)
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

