
import unittest
from setup_imports import setup_imports
setup_imports()

from model.Course import Course
from model.Factory import Factory
from model.EntityType import EntityType


class CourseTests(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_data = 'tests/mock_data.json'

    def test_init(self):
        course = Course(id=1, name='Individual Project', teacher_id=1)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.id, 1)
        self.assertEqual(course.name, 'Individual Project')
        self.assertEqual(course.teacher_id, 1)

    def test_from_json(self):
        courses = Factory.from_json(entity_type=EntityType.COURSE, path=self.mock_data)
        self.assertEqual(len(courses), 4)
        self.assertIsInstance(courses[0], Course)
        self.assertEqual(courses[0].id, 1)
        self.assertEqual(courses[0].name, 'Dstributed Ledgers and CryptoCurrencies')
        self.assertEqual(courses[0].teacher_id, 1)
