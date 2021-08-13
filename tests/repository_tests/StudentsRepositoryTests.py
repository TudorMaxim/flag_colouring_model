import unittest
from model.Student import Student
from setup_imports import setup_imports
setup_imports()

from repository.StudentsRepository import StudentsRepository


class StudentRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = StudentsRepository(dataset='tests/mock_data.json')
        self.student_name = 'Tudor Maxim'

    def test_add(self):
        self.assertEqual(len(self.repository.get_list()), 5)
        self.repository.add(name=self.student_name, course_ids=[1, 2, 3])
        self.assertEqual(len(self.repository.get_list()), 6)
    
    def test_find_by_id(self):
        student = self.repository.find(id=1)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, 1)
        self.assertEqual(student.name, self.student_name)
        self.assertEqual(student.course_ids, [1, 4])
        nobody = self.repository.find(id=1000)
        self.assertNotIsInstance(nobody, Student)
        self.assertIsNone(nobody)
    
    def test_remove(self):
        self.assertIsInstance(self.repository.find(id=1), Student)
        self.repository.remove(id=1)
        self.assertIsNone(self.repository.find(id=1))
    
    def test_update(self):
        student = self.repository.find(id=1)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, 1)
        self.assertEqual(student.name, self.student_name)
        self.assertEqual(student.course_ids, [1, 4])
        self.repository.update(student=Student(id=1, name='MR. ' + self.student_name, course_ids=[1]))
        student = self.repository.find(id=1)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, 1)
        self.assertEqual(student.name, 'MR. ' + self.student_name)
        self.assertEqual(student.course_ids, [1])

    def test_get_list(self):
        students = self.repository.get_list()
        self.assertEqual(len(students), 5)