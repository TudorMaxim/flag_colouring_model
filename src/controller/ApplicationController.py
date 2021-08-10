
from model.Course import Course
from model.Person import Person
from model.Student import Student
from model.Teacher import Teacher
from repository.CoursesRepository import CoursesRepository
from repository.StudentsRepository import StudentsRepository
from repository.TeachersRepository import TeachersRepository
from utils import Constants


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

    
