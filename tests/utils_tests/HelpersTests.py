import unittest
from setup_imports import setup_imports
setup_imports()

from utils.Helpers import Helpers
from model.Student import Student


class HelpersTests(unittest.TestCase):
    def test_build_id_maps(self):
        students = [Student(id=1, name='Student 1'), Student(id=2, name='Student 2')]
        students_map = Helpers.build_ids_map(students)
        self.assertEqual(students[0], students_map[1])
        self.assertEqual(students[1], students_map[2])
    
    def test_get_used_colours(self):
        colouring = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3}
        colours = Helpers.get_used_colours(colouring)
        self.assertListEqual(colours, [1, 2, 3])
    
    def test_get_used_colours_count(self):
        colouring = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3}
        count = Helpers.get_used_colours_count(colouring)
        self.assertEqual(count, 3)
    
    def test_get_hour_and_day(self):
        days = [i for i in range(5)]
        hours = [i for i in range(12)]
        colours = [i + 1 for i in range(60)]
        i = 0
        for day in days:
            for hour in hours:
                h, d = Helpers.get_hour_and_day(colours[i])
                self.assertEqual(d, day)
                self.assertEqual(h, hour)
                i += 1

    def test_map_colour_to_timeslot(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        hours = [
            '08:00AM', '09:00AM', '10:00AM', '11:00AM',
            '12:00PM', '01:00PM', '02:00PM', '03:00PM',
            '04:00PM', '05:00PM', '06:00PM', '07:00PM'
        ]
        colours = [i + 1 for i in range(60)]
        i = 0
        for day in days:
            for hour in hours:
                timeslot = Helpers.map_colour_to_timeslot(colours[i])
                self.assertEqual(timeslot, f'{day} - {hour}')
                i += 1
