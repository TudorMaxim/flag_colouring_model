import unittest
from setup_imports import setup_imports
setup_imports()

from model.Teacher import Teacher
from repository.TeachersRepository import TeachersRepository


class TeachersRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TeachersRepository(dataset='tests/mock_data.json')
        self.teacher_name = 'Prof. Jon Doe'
    
    def test_add(self):
        self.assertEqual(len(self.repository.get_list()), 2)
        self.repository.add(name=self.teacher_name, course_ids=[1, 2, 3])
        self.assertEqual(len(self.repository.get_list()), 3)
    
    def test_find_by_id(self):
        teacher = self.repository.find(id=1)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 1)
        self.assertEqual(teacher.name, self.teacher_name)
        self.assertEqual(teacher.course_ids, [1, 3])
        nobody = self.repository.find(id=1000)
        self.assertNotIsInstance(nobody, Teacher)
        self.assertIsNone(nobody)
    
    def test_remove(self):
        self.assertIsInstance(self.repository.find(id=1), Teacher)
        self.repository.remove(id=1)
        self.assertIsNone(self.repository.find(id=1))
    
    def test_update(self):
        teacher = self.repository.find(id=1)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 1)
        self.assertEqual(teacher.name, self.teacher_name)
        self.assertEqual(teacher.course_ids, [1, 3])
        self.repository.update(teacher=Teacher(id=1, name='MR. ' + self.teacher_name, course_ids=[1]))
        teacher = self.repository.find(id=1)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 1)
        self.assertEqual(teacher.name, 'MR. ' + self.teacher_name)
        self.assertEqual(teacher.course_ids, [1])

    def test_get_list(self):
        teachers = self.repository.get_list()
        self.assertEqual(len(teachers), 2)
