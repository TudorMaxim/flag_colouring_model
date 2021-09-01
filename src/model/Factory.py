import json
from typing import Any, List
from model.Course import Course
from model.Teacher import Teacher
from model.Student import Student
from model.EntityType import EntityType
from utils import Constants

class Factory:
    @staticmethod
    def from_json(entity_type: EntityType, path: str = Constants.DEFAULT_DATASET) -> List[Any]:
        if entity_type == EntityType.STUDENT:
            return Factory.__students_from_json(path)
        elif entity_type == EntityType.TEACHER:
            return Factory.__teachers_from_json(path)
        return Factory.__courses_from_json(path)
    
    @staticmethod
    def __students_from_json(path=Constants.DEFAULT_DATASET) -> List[Student]:
        f = open(path, 'r')
        data = json.load(f)
        students = [Student(student['id'], student['name'], student['course_ids']) for student in data['students']]
        f.close()
        return students

    @staticmethod
    def __teachers_from_json(path=Constants.DEFAULT_DATASET) -> List[Teacher]:
        f = open(path, 'r')
        data = json.load(f)
        teachers = [Teacher(teacher['id'], teacher['name'], teacher['course_ids'], teacher['weights']) for teacher in data['teachers']]
        f.close()
        return teachers
    
    @staticmethod
    def __courses_from_json(path=Constants.DEFAULT_DATASET) -> List[Course]:
        f = open(path, 'r')
        data = json.load(f)
        courses = [Course(course['id'], course['name'], course['teacher_id']) for course in data['courses']]
        f.close()
        return courses
