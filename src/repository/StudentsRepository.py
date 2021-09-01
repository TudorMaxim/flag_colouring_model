from model.EntityType import EntityType
from model.Factory import Factory
from model.Student import Student
from utils import Constants
from utils.Helpers import Helpers
from typing import List

class StudentsRepository:
    def __init__(self, dataset: str = Constants.DEFAULT_DATASET) -> None:
        self.students = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.STUDENT, path=dataset))

    def add(self, name: str, course_ids: List[int]) -> None:
        student_with_max_id = max(self.students.values(), key=lambda student: student.id)
        student_id = 1 + student_with_max_id.id
        student = Student(id=student_id, name=name, course_ids=course_ids)
        self.students[student_id] = student
    
    def remove(self, id: int) -> None:
        self.students.pop(id)
    
    def update(self, student: Student) -> None:
        self.students[student.id] = student
    
    def find(self, id: int) -> Student:
        return self.students.get(id)

    def get_list(self) -> List[Student]:
        return self.students.values()
    
    def change_dataset(self, dataset: str) -> None:
        self.students = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.STUDENT, path=dataset))
