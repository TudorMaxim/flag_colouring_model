import unittest
from setup_imports import setup_imports
setup_imports()

from algorithms.DegreeOfSaturation import DegreeOfSaturation
from utils.Helpers import Helpers
from utils.Conflicts import Conflicts
from model.EntityType import EntityType
from model.Factory import Factory


class DegreeOfSaturationTests(unittest.TestCase):
    def test_algorithm(self):
        dataset = 'tests/mock_data.json'
        students = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.STUDENT, path=dataset))
        teachers = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.TEACHER, path=dataset))
        courses = Helpers.build_ids_map(Factory.from_json(entity_type=EntityType.COURSE, path=dataset))
        conflict_graph = Conflicts.build_graph(list(students.values()), list(teachers.values()))
        algorithm = DegreeOfSaturation(
            graph=conflict_graph,
            students_map=students,
            teachers_map=teachers,
            courses_map=courses
        )
        colour_set = Helpers.generate_colour_set(teachers.values())
        colouring = algorithm.run(colours_set=colour_set)
        self.assertTrue(conflict_graph.valid_colouring(colour_map=colouring))
