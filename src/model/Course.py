import json
from utils import Constants
from typing import Optional

class Course:
    def __init__(self, id: int, name: str, teacher_id: Optional[int]):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id

    def __str__(self):
        return f'Course#{self.id}'

    
