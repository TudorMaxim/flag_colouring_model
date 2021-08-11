from random import randint, shuffle, choice
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem
from typing import List, Tuple, Callable
from utils import Constants
from model.Student import Student
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
    def get_hour_and_day(colour: int) -> Tuple[int, int]:
        assert colour <= 60 and colour >= 1
        day = (colour - 1) // 12
        hour = (colour - 1) % 12
        return hour, day
 
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

    # Function that generates n entities based on a list of default names
    @staticmethod
    def generate_entities(n: int, default_names: List[str]) -> List:
        cnt = [1 for _ in range(len(default_names))]
        entities = []
        for id in range(1, n + 1):
            index = randint(0, len(default_names) - 1)
            name = default_names[index] + f'#{cnt[index]}'
            cnt[index] += 1
            entities.append({
                'id': id,
                'name': name
            })
        return entities


    # Function that randomly assings courses to students
    # A student may have many courses and a course may have many students
    @staticmethod
    def assign_courses_to_students(students: List, c: int, minn: int, maxx: int) -> List:
        course_ids = [i + 1 for i in range(c)]
        assignments = []
        for student in students:
            shuffle(course_ids)
            cnt = randint(minn, min(c - 1, maxx))
            assignments.append({
                'id': student['id'],
                'name': student['name'],
                'course_ids': course_ids[0:cnt]
            })
        return assignments

    # Function that randomly assigns courses to teachers
    # A teacher can have multiple courses, but a course can be held only by one teacher
    @staticmethod
    def assign_courses_to_teachers(teachers: List, c: int, t: int) -> List:
        course_ids = [i + 1 for i in range(c)]
        shuffle(course_ids)
        for i in range(c):
            idx = i % t
            if 'course_ids' in teachers[idx]:
                teachers[idx]['course_ids'].append(course_ids[i])
            else:
                teachers[idx]['course_ids'] = [course_ids[i]]
        return teachers

    # Function that finds the id of the teacher who is responsible with a course.
    @staticmethod
    def find_teacher_id(teachers: List, course_id: int) -> int:
        for teacher in teachers:
            if course_id in teacher['course_ids']:
                return teacher['id']
        raise ValueError(
            f'Error: Could not find a teacher for course with id {course_id}.')

    # Function that randomly generates preferences for teachers.
    # 2 - preferred time slot
    # 4 - indifferent
    # 8 - unpreferred time slot
    @staticmethod
    def generate_weights(teachers: List) -> List:
        options = [2, 4, 8]
        for i in range(len(teachers)):
            # The first element will always be 0 because colours start from 1
            weights = [0] * (Constants.COLOURS_CNT + 1)
            for j in range(1, len(weights)):
                weights[j] = choice(options)
            teachers[i]['weights'] = weights
        return teachers

    @staticmethod
    def show_error_message(message: str, informative_text: str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle("Error")
        msg.exec_()

    # QListWdiget Helpers
    @staticmethod
    def populate(list_widget: QListWidget, entities: List, mapper: Callable):
        list_widget.clear()
        items = list(map(mapper, entities))
        for item in items:
            list_widget.addItem(item)
    
    @staticmethod
    def map_student_to_list_item(student: Student) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(student.name)
        item.setData(Qt.UserRole, student)
        return item
    
    @staticmethod
    def map_course_to_list_item(course: Course) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(course.name)
        item.setData(Qt.UserRole, course)
        return item

    @staticmethod
    def map_teacher_to_list_item(teacher: Teacher) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(teacher.name)
        item.setData(Qt.UserRole, teacher)
        return item
