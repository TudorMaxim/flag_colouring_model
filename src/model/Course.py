import json


class Course:
    def __init__(self, id: int, name: str, teacher_id: int):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id

    def __str__(self):
        return f'Course#{self.id}'

    @staticmethod
    def from_json(path='datasets/small_dataset.json'):
        f = open(path, 'r')
        data = json.load(f)
        return [Course(course['id'], course['name'], course['teacher_id']) for course in data['courses']]
    
