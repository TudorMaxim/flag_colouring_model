import unittest
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from setup_imports import setup_imports
from utils import Constants
setup_imports()

from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm, EvolutionaryAlgorithmConfig
from utils.Helpers import Helpers
from utils.Conflicts import Conflicts
from model.Teacher import Teacher
from model.Course import Course
from model.Student import Student

class EvolutionaryAlgorithmTests(unittest.TestCase):
    def test_algorithm(self):
        dataset = 'tests/mock_data.json'
        students = Helpers.build_ids_map(Student.from_json(dataset))
        teachers = Helpers.build_ids_map(Teacher.from_json(dataset))
        courses = Helpers.build_ids_map(Course.from_json(dataset))
        conflict_graph = Conflicts.build_graph(list(students.values()), list(teachers.values()))
        algorithm = EvolutionaryAlgorithm(
            graph=conflict_graph,
            students_map=students,
            teachers_map=teachers,
            courses_map=courses,
        )
        algorithm.debug = False
        algorithm.generations_cnt = Constants.GENERATIONS_CNT
        algorithm.population_cnt = Constants.POPULATION_CNT
        algorithm.mutation_probability = Constants.MUTATION_PROBABILITY
        algorithm.population_model = EvolutionaryAlgorithmConfig.STEADY_STATE_POPULATION
        algorithm.selection_method = EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SELECTION
        
        colour_set = Helpers.generate_colour_set(teachers.values())

        colouring = algorithm.run(colours_set=colour_set)
        self.assertTrue(conflict_graph.valid_colouring(colour_map=colouring[0]))

        algorithm.selection_method = EvolutionaryAlgorithmConfig.TOURNAMENT_SELECTION
        colouring = algorithm.run(colours_set=colour_set)
        self.assertTrue(conflict_graph.valid_colouring(colour_map=colouring[0]))

        algorithm.population_model = EvolutionaryAlgorithmConfig.GENERATIONAL_POPULATION
        colouring = algorithm.run(colours_set=colour_set)
        self.assertTrue(conflict_graph.valid_colouring(colour_map=colouring[0]))
