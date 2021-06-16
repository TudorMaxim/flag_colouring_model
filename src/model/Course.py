import json

class Course:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f'Course#{self.id}'

    @staticmethod
    def from_json(path='datasets/small_dataset.json'):
        f = open(path, 'r')
        data = json.load(f)
        return [Course(course['id'], course['name']) for course in data['courses']]
    
    @staticmethod
    def build_ids_map(courses):
        ids_map = {}
        for course in courses:
            ids_map[course.id] = course
        return ids_map
