import json
from utils import Constants

class Room:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @staticmethod
    def from_json(path=Constants.DEFAULT_DATASET):
        f = open(path, 'r')
        data = json.load(f)
        return [Room(room['id'], room['name']) for room in data['rooms']]
        