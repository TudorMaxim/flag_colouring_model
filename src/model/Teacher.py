import json
from model.Person import Person

class Teacher(Person):
    def __init__(self, id: int, name: str, course_ids=None):
        super().__init__(id, name, course_ids)
    
    def __str__(self):
        return f'Teacher(id: {self.id}, name: {self.name})'

    @staticmethod
    def from_json(path='datasets/small_dataset.json'):
        f = open(path, 'r')
        data = json.load(f)
        return [Teacher(teacher['id'], teacher['name'], teacher['course_ids']) for teacher in data['teachers']]
