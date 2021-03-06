from typing import List
from model.Course import Course
from model.EntityType import EntityType
from model.Factory import Factory
from utils.Helpers import Helpers
from utils import Constants


class CoursesRepository:
    def __init__(self, dataset: str = Constants.DEFAULT_DATASET) -> None:
        self.courses = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.COURSE, path=dataset))
    
    def add(self, name: str, teacher_id: int) -> None:
        course_with_max_id = max(self.courses.values(), key=lambda course: course.id)
        course_id = 1 + course_with_max_id.id
        course = Course(id=course_id, name=name, teacher_id=teacher_id)
        self.courses[course_id] = course

    def remove(self, id: int) -> None:
        self.courses.pop(id)

    def update(self, course: Course) -> None:
        self.courses[course.id] = course

    def find(self, id: int) -> Course:
        return self.courses.get(id)

    def get_list(self) -> List[Course]:
        return self.courses.values()

    def change_dataset(self, dataset: str) -> None:
        self.courses = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.COURSE, path=dataset))
