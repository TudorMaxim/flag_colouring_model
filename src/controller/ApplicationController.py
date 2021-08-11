
import json
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
    def __init__(self, dataset: str = Constants.DEFAULT_DATASET) -> None:
        self.dataset = dataset
        self.students_repository = StudentsRepository(dataset)
        self.teachers_repository = TeachersRepository(dataset)
        self.courses_repository = CoursesRepository(dataset)
    
    def change_dataset(self, dataset: str) -> None:
        self.dataset = dataset
        self.students_repository.change_dataset(dataset)
        self.teachers_repository.change_dataset(dataset)
        self.courses_repository.change_dataset(dataset)

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
    
