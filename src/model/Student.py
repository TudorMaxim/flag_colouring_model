import json
from model.Person import Person
from utils import Constants

class Student(Person):
    def __init__(self, id: int, name: str, course_ids=[]):
        super().__init__(id, name, course_ids)
    
    def __str__(self):
        return f'Student(id: {self.id}, name: {self.name})'
