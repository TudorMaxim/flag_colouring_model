import json

class Room:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @staticmethod
    def from_json(path='datasets/small1/entities.json'):
        f = open(path, 'r')
        data = json.load(f)
        return [Room(room['id'], room['name']) for room in data['rooms']]
        