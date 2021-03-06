from model.EntityType import EntityType
from model.Factory import Factory
from model.Teacher import Teacher
from utils import Constants
from utils.Helpers import Helpers
from typing import List


class TeachersRepository:
    def __init__(self, dataset: str = Constants.DEFAULT_DATASET) -> None:
        self.teachers = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.TEACHER, path=dataset))

    def add(self, name: str, course_ids: List[int]) -> None:
        teacher_with_max_id = max(self.teachers.values(), key=lambda teacher: teacher.id)
        teacher_id = 1 + teacher_with_max_id.id
        teacher = Teacher(id=teacher_id, name=name, course_ids=course_ids)
        self.teachers[teacher_id] = teacher

    def remove(self, id: int) -> None:
        self.teachers.pop(id)
        
    def update(self, teacher: Teacher) -> None:
        self.teachers[teacher.id] = teacher

    def find(self, id: int) -> Teacher:
        return self.teachers.get(id)

    def get_list(self) -> List[Teacher]:
        return self.teachers.values()
    
    def change_dataset(self, dataset: str) -> None:
        self.teachers = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.TEACHER, path=dataset))
