
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
