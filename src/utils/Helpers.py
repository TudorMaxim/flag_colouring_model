from os import stat
from typing import List
from utils import Constants
from model.Teacher import Teacher
from model.Course import Course


class Helpers:
    @staticmethod
    def build_ids_map(entities: List):
        ids_map = {}
        for entity in entities:
            ids_map[entity.id] = entity
        return ids_map

    @staticmethod
    def get_used_colours(colouring: dict[int, int]) -> List:
        used_colours = []
        for course_id in colouring:
            if colouring[course_id] not in used_colours:
                used_colours.append(colouring[course_id])
        return used_colours

    @staticmethod
    def get_used_colours_count(colouring: dict[int, int]) -> int:
        return len(Helpers.get_used_colours(colouring))

    @staticmethod
    def __compute_teachers_preference(teachers: List[Teacher], colour: int) -> float:
        day = (colour - 1) // 12 + 1
        hour = (colour - 1) % 12 + 1
        weights = list(map(lambda teacher: teacher.weights[colour], teachers))
        denominator = sum(weights)
        numerator = 0
        for weight in weights:
            numerator += weight * day * hour
        return numerator / denominator

    
    @staticmethod
    def generate_colour_set(teachers: List[Teacher]) -> List[int]:
        colours_set = [i for i in range(1, Constants.COLOURS_CNT + 1)]
        return sorted(colours_set, key=lambda colour: Helpers.__compute_teachers_preference(teachers, colour))

    @staticmethod
    def build_positions_map(colours_sets: List[List[int]]) -> List[dict[int, int]]:
        positions = []
        for i in range(3):
            position = {}
            for j in range(len(colours_sets[i])):
                position[colours_sets[i][j]] = j
            positions.append(position)
        return positions
    
    @staticmethod
    def map_colour_to_timeslot(colour: int) -> str:
        assert colour <= 60 and colour >= 1
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        hours = [
            '08:00AM', '09:00AM', '10:00AM', '11:00AM',
            '12:00PM', '01:00PM', '02:00PM', '03:00PM',
            '04:00PM', '05:00PM', '06:00PM', '07:00PM'
        ]
        day = (colour - 1) // 12
        hour = (colour - 1) % 12
        return f'{days[day]} - {hours[hour]}'

    @staticmethod
    def print_timetable(courses_map: dict[int, Course], colouring: dict[int, int]) -> None:
        print('TIMETABLE:')
        for id in courses_map:
            course = courses_map[id]
            scheduled_time = Helpers.map_colour_to_timeslot(colouring[id])
            print(f'{course}: {scheduled_time}')

