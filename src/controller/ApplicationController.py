
import json
from typing import List, Optional
from model.Course import Course
from model.Person import Person
from model.Student import Student
from model.Teacher import Teacher
from repository.CoursesRepository import CoursesRepository
from repository.StudentsRepository import StudentsRepository
from repository.TeachersRepository import TeachersRepository
from utils import Constants
from utils.Helpers import Helpers


class ApplicationController:
    def __init__(self, dataset_path: str = Constants.DEFAULT_DATASET) -> None:
        self.dataset_path = dataset_path
        self.students_repository = StudentsRepository(dataset_path)
        self.teachers_repository = TeachersRepository(dataset_path)
        self.courses_repository = CoursesRepository(dataset_path)
    
    def change_dataset(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path
        self.students_repository.change_dataset(dataset_path)
        self.teachers_repository.change_dataset(dataset_path)
        self.courses_repository.change_dataset(dataset_path)

    def get_students(self) -> dict[int, Student]:
        return self.students_repository.students
    
    def get_teachers(self) -> dict[int, Teacher]:
        return self.teachers_repository.teachers
    
    def get_courses(self) -> dict[int, Course]:
        return self.courses_repository.courses

    def get_student(self, student_id: int) -> Student:
        return self.students_repository.students[student_id]
    
    def get_teacher(self, teacher_id: int) -> Teacher:
        return self.teachers_repository.teachers[teacher_id]
    
    def get_course(self, course_id: int) -> Course:
        return self.courses_repository.courses[course_id]
    
    def get_courses_for(self, person: Person) -> dict[int, Course]:
        courses = self.get_courses()
        filtered = {}
        for id in courses:
            if id in person.course_ids:
                filtered[id] = courses[id]
        return filtered

    def get_teacher_of(self, course: Course) -> Teacher:
        for teacher in self.get_teachers().values():
            if teacher.id == course.teacher_id:
                return teacher
        return None
    
    def add_student(self, name: str, course_ids: List[int]):
        assert name != '', 'Error: Student name cannot be blank!'
        assert len(course_ids), 'Error: A student must be enroled in at least one course!'
        for course_id in course_ids:
            assert \
                course_id in list(map(lambda course: course.id, self.get_courses().values())), \
                f'Error: Course with id {course_id} does not exist!'
        self.students_repository.add(name, course_ids)

    def add_teacher(self, name: str, course_ids: List[int]):
        assert name != '', 'Error: Teacher name cannot be blank!'
        for course_id in course_ids:
            assert \
                course_id in list(map(lambda course: course.id, self.get_courses().values())), \
                f'Error: Course with id {course_id} does not exist!'
        self.teachers_repository.add(name, course_ids)
    
    def add_course(self, name: str, teacher_id: Optional[int]):
        assert name != '', 'Error: Course name cannot be blank!'
        if teacher_id is not None:
            assert \
                teacher_id in list(map(lambda teacher: teacher.id, self.get_teachers().values())), \
                f'Error: teacher with id {teacher_id} does not exist!'
        self.courses_repository.add(name, teacher_id)

    def update(self, entity, name: str) -> None:
        entity.name = name
        if isinstance(entity, Student):
            self.students_repository.students[entity.id].name = name
        elif isinstance(entity, Teacher):
            self.teachers_repository.teachers[entity.id].name = name
        elif isinstance(entity, Course):
            self.courses_repository.courses[entity.id].name = name
    
    def delete(self, entity) -> None:
        if isinstance(entity, Student):
            self.students_repository.remove(entity.id)
        elif isinstance(entity, Teacher):
            self.teachers_repository.remove(entity.id)
        elif isinstance(entity, Course):
            self.courses_repository.remove(entity.id)
            for course in self.get_courses().values():
                if course.teacher_id == entity.id:
                    course.teacher_id = None
            for student in self.get_students().values():
                if entity.id in student.course_ids:
                    student.course_ids.remove(entity.id)
            for teacher in self.get_teachers().values():
                if entity.id in teacher.course_ids:
                    teacher.course_ids.remove(entity.id)
    
    def generate_dataset(self, s: int, t: int, c: int, min_enrolment: int, max_enrolment: int) -> dict:
        assert s >= c, 'The number of students should be greater than or equal to the number of courses.'
        assert t <= c, 'The number of teachers should be less than or equal to the number of courses.'
        assert s > t, 'The number of students must be greater than the number of teachers.'
        courses = Helpers.generate_entities(c, default_names=[
            'Big Data Technologies',
            'Model Driven Development',
            'Software Engineering',
            'Distributed Ledgers',
            'Security Engineering',
            'Security Management',
            'Software Testing',
            'Artificial Intelligence'
        ])
        students = Helpers.generate_entities(s, default_names=[
            'Tudor Maxim',
            'Jon Doe',
            'Jane Doe',
            'Mark Doe',
            'Mary Doe'
        ])
        teachers = Helpers.generate_entities(t, default_names=[
            'Jon Smith',
            'Jane Smith',
            'Mark Smith'
        ])
        teachers = Helpers.assign_courses_to_teachers(teachers, c, t)
        teachers = Helpers.generate_weights(teachers)
        students = Helpers.assign_courses_to_students(students, c, min_enrolment, max_enrolment)
        for i in range(len(courses)):
            courses[i]['teacher_id'] = Helpers.find_teacher_id(
                teachers, courses[i]['id'])
        return {
            'courses': courses,
            'teachers': teachers,
            'students': students,
        }
    
    def save_dataset(self, dataset: dict, path: str) -> None:
        with open(path, 'w') as file:
            json.dump(dataset, file, indent=4)
    
    def get_dataset(self) -> dict:
        students = list(map(lambda x: vars(x), self.students_repository.get_list()))
        teachers = list(map(lambda x: vars(x), self.teachers_repository.get_list()))
        courses = list(map(lambda x: vars(x), self.courses_repository.get_list()))
        return {
            'students': students,
            'teachers': teachers,
            'courses': courses
        }

    def assign_courses_to_student(self, student: Student, courses: List[Course]) -> None:
        course_ids = list(map(lambda course: course.id, courses))
        student.course_ids.extend(course_ids)
        self.students_repository.update(student=student)
    
    def assign_courses_to_teacher(self, teacher: Teacher, courses: List[Course]) -> None:
        course_ids = list(map(lambda course: course.id, courses))
        teacher.course_ids.extend(course_ids)
        self.teachers_repository.update(teacher=teacher)
        for course in courses:
            course.teacher_id = teacher.id
            self.courses_repository.update(course)
    
    def assign_teacher_to_course(self, course: Course, teacher: Teacher) -> None:
        course.teacher_id = teacher.id
        self.courses_repository.update(course=course)
        teacher.course_ids.append(course.id)
        self.teachers_repository.update(teacher=teacher)
