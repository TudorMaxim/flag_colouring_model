import unittest
from setup_imports import setup_imports
setup_imports()

from model.Teacher import Teacher
from utils.Constants import COLOURS_CNT
from model.Factory import Factory
from model.EntityType import EntityType


class TeacherTests(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_data = 'tests/mock_data.json'

    def test_init(self):
        teacher = Teacher(id=1, name='Tudor Maxim', course_ids=[1, 2, 3])
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 1)
        self.assertEqual(teacher.name, 'Tudor Maxim')
        self.assertEqual(teacher.course_ids, [1, 2, 3])
        self.assertEqual(teacher.weights, None)

    def test_from_json(self):
        teachers = Factory.from_json(entity_type=EntityType.TEACHER, path=self.mock_data)
        self.assertEqual(len(teachers), 2)
        self.assertIsInstance(teachers[0], Teacher)
        self.assertEqual(teachers[0].id, 1)
        self.assertEqual(teachers[0].name, 'Prof. Jon Doe')
        self.assertEqual(teachers[0].course_ids, [1, 3])
        self.assertEqual(len(teachers[0].weights), COLOURS_CNT + 1) # colours start from 1
        self.assertTrue(all(weight in [0, 2, 4, 8] for weight in teachers[0].weights))
