import unittest
from setup_imports import setup_imports
setup_imports()

from controller.TimetablingController import TimetablingController
from controller.ApplicationController import ApplicationController


class TimetablingControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        dataset = 'tests/mock_data.json'
        app_controller = ApplicationController(dataset_path=dataset)
        self.student = app_controller.get_student(student_id=1)
        self.teacher = app_controller.get_teacher(teacher_id=1)
        self.controller = TimetablingController(
            students=app_controller.get_students(),
            teachers=app_controller.get_teachers(),
            courses=app_controller.get_courses()
        )
    
    def test_schedule(self):
        timetabling = self.controller.schedule()
        self.assertTrue(self.controller.conflict_graph.valid_colouring(timetabling))

    def test_get_student_timetable(self):
        timetable = self.controller.get_student_timetable(student_id=self.student.id)
        self.assertEqual(timetable, {})
        self.controller.schedule()
        timetable = self.controller.get_student_timetable(student_id=self.student.id)
        self.assertIsNotNone(timetable)
        self.assertCountEqual(self.student.course_ids, timetable.keys())
        self.assertEqual(sorted(self.student.course_ids), sorted(timetable.keys()))
    
    def test_get_teacher_timetable(self):
        timetable = self.controller.get_teacher_timetable(teacher_id=self.teacher.id)
        self.assertEqual(timetable, {})
        self.controller.schedule()
        timetable = self.controller.get_teacher_timetable(teacher_id=self.teacher.id)
        self.assertIsNotNone(timetable)
        self.assertCountEqual(self.teacher.course_ids, timetable.keys())
        self.assertEqual(sorted(self.teacher.course_ids), sorted(timetable.keys()))