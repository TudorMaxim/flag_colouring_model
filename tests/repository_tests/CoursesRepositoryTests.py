import unittest
from setup_imports import setup_imports
setup_imports()

from model.Course import Course
from repository.CoursesRepository import CoursesRepository


class CoursesRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CoursesRepository(dataset='tests/mock_data.json')
        self.course_name = 'Individual Project'
    
    def test_add(self):
        self.assertEqual(len(self.repository.get_list()), 4)
        self.repository.add(name=self.course_name, teacher_id=1)
        self.assertEqual(len(self.repository.get_list()), 5)
    
    def test_find_by_id(self):
        course = self.repository.find(id=1)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.id, 1)
        self.assertEqual(course.name, 'Dstributed Ledgers and CryptoCurrencies')
        self.assertEqual(course.teacher_id, 1)
        none = self.repository.find(id=1000)
        self.assertNotIsInstance(none, Course)
        self.assertIsNone(none)
    
    def test_remove(self):
        self.assertIsInstance(self.repository.find(id=1), Course)
        self.repository.remove(id=1)
        self.assertIsNone(self.repository.find(id=1))
    
    def test_update(self):
        course = self.repository.find(id=1)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.id, 1)
        self.assertEqual(course.name, 'Dstributed Ledgers and CryptoCurrencies')
        self.assertEqual(course.teacher_id, 1)
        self.repository.update(course=Course(id=1, name=self.course_name, teacher_id=2))
        course = self.repository.find(id=1)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.id, 1)
        self.assertEqual(course.name, self.course_name)
        self.assertEqual(course.teacher_id, 2)

    def test_get_list(self):
        courses = self.repository.get_list()
        self.assertEqual(len(courses), 4)
