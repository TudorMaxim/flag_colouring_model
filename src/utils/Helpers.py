from typing import List


class Helpers:
    @staticmethod
    def build_ids_map(entities: List):
        ids_map = {}
        for entity in entities:
            ids_map[entity.id] = entity
        return ids_map

    @staticmethod
    def get_used_colours(colouring: dict[int, int]) -> List:
        used_colours = []
        for course_id in colouring:
            if colouring[course_id] not in used_colours:
                used_colours.append(colouring[course_id])
        return used_colours

    @staticmethod
    def get_used_colours_count(colouring: dict[int, int]) -> int:
        return len(Helpers.get_used_colours(colouring))
