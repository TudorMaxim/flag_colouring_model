from model.Person import Person

class Student(Person):
    def __init__(self, id: int, name: str, course_ids=[]):
        super().__init__(id, name, course_ids)
    
    def __str__(self):
        return f'Student(id: {self.id}, name: {self.name})'
