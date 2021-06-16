from typing import List


class Person:
    def __init__(self, id: int, name: str, course_ids: List[int] = None):
        self.id = id
        self.name = name
        self.course_ids = course_ids

