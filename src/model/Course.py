import json

class Course:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @staticmethod
    def from_json(path='datasets/small1/entities.json'):
        f = open(path, 'r')
        data = json.load(f)
        return [Course(course['id'], course['name']) for course in data['courses']]
