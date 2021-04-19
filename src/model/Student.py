from model.Person import Person

class Student(Person):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
    
    def __str__(self):
        return f'Student(id: {self.id}, name: {self.name})'
