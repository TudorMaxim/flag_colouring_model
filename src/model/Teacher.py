import json
from model.Person import Person
from utils import Constants

class Teacher(Person):
    def __init__(self, id: int, name: str, course_ids=None, weights=None):
        super().__init__(id, name, course_ids)
        self.weights = weights
    
    def __str__(self):
        return f'Teacher(id: {self.id}, name: {self.name})'

