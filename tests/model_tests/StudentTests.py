from setup_imports import setup_imports
setup_imports()

import unittest
from model.Student import Student
from model.Factory import Factory
from model.EntityType import EntityType


class StudentTests(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_data = 'tests/mock_data.json'
    
    def test_init(self):
        student = Student(id=1, name='Tudor Maxim', course_ids=[1, 2, 3])
        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, 1)
        self.assertEqual(student.name, 'Tudor Maxim')
        self.assertEqual(student.course_ids, [1, 2, 3])
    
    def test_from_json(self):
        students = Factory.from_json(entity_type=EntityType.STUDENT, path=self.mock_data)
        self.assertEqual(len(students), 5)
        self.assertIsInstance(students[0], Student)
        self.assertEqual(students[0].id, 1)
        self.assertEqual(students[0].name, 'Tudor Maxim')
        self.assertEqual(students[0].course_ids, [1, 4])
