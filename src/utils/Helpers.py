from typing import List


class Helpers:
    @staticmethod
    def build_ids_map(entities: List):
        ids_map = {}
        for entity in entities:
            ids_map[entity.id] = entity
        return ids_map
