import json
from model.Person import Person

class Teacher(Person):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
    
    def __str__(self):
        return f'Teacher(id: {self.id}, name: {self.name})'

    @staticmethod
    def from_json(path='datasets/small1/entities.json'):
        f = open(path, 'r')
        data = json.load(f)
        return [Teacher(teacher['id'], teacher['name']) for teacher in data['teachers']]