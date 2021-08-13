import unittest
from model.Student import Student
from setup_imports import setup_imports
setup_imports()

from controller.ApplicationController import ApplicationController
from model.Course import Course
from model.Teacher import Teacher


class ApplicationControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        dataset = 'tests/mock_data.json'
        self.person_name = 'Tudor Maxim'
        self.course_name = 'Individual Project'
        self.controller = ApplicationController(dataset_path=dataset)
    
    def test_get_courses_for(self):
        student = self.controller.get_student(student_id=1)
        courses = self.controller.get_courses_for(student)
        self.assertEqual(len(courses), 2)
        self.assertEqual(list(courses.keys()), [1, 4])

        teacher = self.controller.get_teacher(teacher_id=1)
        courses = self.controller.get_courses_for(teacher)
        self.assertEqual(len(courses), 2)
        self.assertEqual(list(courses.keys()), [1, 3])

    def test_get_teacher_of(self):
        course = self.controller.get_course(course_id=1)
        teacher = self.controller.get_teacher_of(course)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 1)

        course = self.controller.get_course(course_id=10000000)
        teacher = self.controller.get_teacher_of(course)
        self.assertIsNone(teacher)

    def test_add_student(self):
        with self.assertRaises(Exception) as context:
            self.controller.add_student(name='', course_ids=[])
        self.assertTrue('Error: Student name cannot be blank!' in str(context.exception))
    
        with self.assertRaises(Exception) as context:
            self.controller.add_student(name=self.person_name, course_ids=[])
        self.assertTrue('Error: A student must be enroled in at least one course!' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.controller.add_student(name=self.person_name, course_ids=[100])
        self.assertTrue('Error: Course with id 100 does not exist!' in str(context.exception))

        self.assertEqual(len(self.controller.get_students().values()), 5)
        self.controller.add_student(name=self.person_name, course_ids=[1, 2])
        self.assertEqual(len(self.controller.get_students().values()), 6)

        student = self.controller.get_student(student_id=6)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, 6)
        self.assertEqual(student.name, self.person_name)
        self.assertEqual(student.course_ids, [1, 2])
    
    def test_add_teacher(self):
        with self.assertRaises(Exception) as context:
            self.controller.add_teacher(name='', course_ids=[])
        self.assertTrue('Error: Teacher name cannot be blank!' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.controller.add_teacher(name=self.person_name, course_ids=[100])
        self.assertTrue('Error: Course with id 100 does not exist!' in str(context.exception))

        self.assertEqual(len(self.controller.get_teachers().values()), 2)
        self.controller.add_teacher(name=self.person_name, course_ids=[1, 2])
        self.assertEqual(len(self.controller.get_teachers().values()), 3)

        teacher = self.controller.get_teacher(teacher_id=3)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 3)
        self.assertEqual(teacher.name, self.person_name)
        self.assertEqual(teacher.course_ids, [1, 2])
    
    def test_add_course(self):
        with self.assertRaises(Exception) as context:
            self.controller.add_course(name='', teacher_id=1)
        self.assertTrue('Error: Course name cannot be blank!' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.controller.add_course(name=self.course_name, teacher_id=100)
        self.assertTrue('Error: teacher with id 100 does not exist!' in str(context.exception))

        self.assertEqual(len(self.controller.get_courses().values()), 4)
        self.controller.add_course(name=self.course_name, teacher_id=1)
        self.assertEqual(len(self.controller.get_courses().values()), 5)

        course = self.controller.get_course(course_id=5)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.id, 5)
        self.assertEqual(course.name, self.course_name)
        self.assertEqual(course.teacher_id, 1)

    def test_update(self):
        new_name = 'NEW NAME'
        student = self.controller.get_student(student_id=1)
        self.assertNotEqual(student.name, new_name)
        self.controller.update(student, new_name)
        self.assertEqual(student.name, new_name)

        teacher = self.controller.get_teacher(teacher_id=1)
        self.assertNotEqual(teacher.name, new_name)
        self.controller.update(teacher, new_name)
        self.assertEqual(teacher.name, new_name)

        course = self.controller.get_course(course_id=1)
        self.assertNotEqual(course.name, new_name)
        self.controller.update(course, new_name)
        self.assertEqual(course.name, new_name)
    
    def test_delete(self):
        self.assertEqual(len(self.controller.get_students().values()), 5)
        student = self.controller.get_student(student_id=1)
        self.controller.delete(student)
        self.assertEqual(len(self.controller.get_students().values()), 4)

        self.assertEqual(len(self.controller.get_teachers().values()), 2)
        teacher = self.controller.get_teacher(teacher_id=1)
        self.controller.delete(teacher)
        self.assertEqual(len(self.controller.get_teachers().values()), 1)
        for course in self.controller.get_courses().values():
            self.assertTrue(course.teacher_id != teacher.id)
        
        self.assertEqual(len(self.controller.get_courses().values()), 4)
        course = self.controller.get_course(course_id=1)
        self.controller.delete(course)
        self.assertEqual(len(self.controller.get_courses().values()), 3)
        for student in self.controller.get_students().values():
            self.assertTrue(course.id not in student.course_ids)
        for teacher in self.controller.get_teachers().values():
            self.assertTrue(course.id not in teacher.course_ids)

    def test_assign_courses_to_student(self):
        self.assertEqual(len(self.controller.get_courses().values()), 4)
        self.controller.add_course(name=self.course_name, teacher_id=None)
        self.assertEqual(len(self.controller.get_courses().values()), 5)

        student = self.controller.get_student(student_id=1)
        course = self.controller.get_course(course_id=5)
        self.assertFalse(course.id in student.course_ids)

        self.controller.assign_courses_to_student(student, [course])
        student = self.controller.get_student(student_id=1)
        course = self.controller.get_course(course_id=5)
        self.assertTrue(course.id in student.course_ids)

    def test_assign_courses_to_teacher(self):
        self.assertEqual(len(self.controller.get_courses().values()), 4)
        self.controller.add_course(name=self.course_name, teacher_id=None)
        self.assertEqual(len(self.controller.get_courses().values()), 5)

        teacher = self.controller.get_teacher(teacher_id=1)
        course = self.controller.get_course(course_id=5)
        self.assertFalse(course.id in teacher.course_ids)
        self.assertIsNone(course.teacher_id)

        self.controller.assign_courses_to_teacher(teacher, [course])
        teacher = self.controller.get_teacher(teacher_id=1)
        course = self.controller.get_course(course_id=5)
        self.assertEqual(course.teacher_id, 1)
        self.assertTrue(course.id in teacher.course_ids)
    
    def test_assign_teacher_to_course(self):
        self.assertEqual(len(self.controller.get_courses().values()), 4)
        self.controller.add_course(name=self.course_name, teacher_id=None)
        self.assertEqual(len(self.controller.get_courses().values()), 5)

        teacher = self.controller.get_teacher(teacher_id=1)
        course = self.controller.get_course(course_id=5)
        self.assertFalse(course.id in teacher.course_ids)
        self.assertIsNone(course.teacher_id)

        self.controller.assign_courses_to_teacher(teacher, [course])
        teacher = self.controller.get_teacher(teacher_id=1)
        course = self.controller.get_course(course_id=5)
        self.assertTrue(course.id in teacher.course_ids)
        self.assertEqual(course.teacher_id, 1)
