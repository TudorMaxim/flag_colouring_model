import unittest
from model.Student import Student
from setup_imports import setup_imports
from utils.Helpers import Helpers
setup_imports()

from utils.Helpers import Helpers
from utils.Conflicts import Conflicts
from model.Chromosome import Chromosome
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course


class ChromosomeTests(unittest.TestCase):
    def setUp(self) -> None:
        dataset = 'tests/mock_data.json'
        self.students = Helpers.build_ids_map(Student.from_json(path=dataset))
        self.teachers = Helpers.build_ids_map(Teacher.from_json(path=dataset))
        self.courses = Helpers.build_ids_map(Course.from_json(path=dataset))
        self.conflict_graph = Conflicts.build_graph(students=self.students.values(), teachers=self.teachers.values())
        self.chromosome_valid = Chromosome(
            graph=self.conflict_graph,
            students_map=self.students,
            teachers_map=self.teachers,
            courses_map=self.courses,
            genes={1: 1, 2: 2, 3: 2, 4: 3}
        )
        self.chromosome_invalid = Chromosome(
            graph=self.conflict_graph,
            students_map=self.students,
            teachers_map=self.teachers,
            courses_map=self.courses,
            genes={1: 1, 2: 1, 3: 2, 4: 3}
        )
    
    def test_fitness(self):
        self.assertEqual(self.chromosome_valid.fitness(), 213.0)
        self.assertAlmostEqual(self.chromosome_invalid.fitness(), 2260.090909090909)
        self.assertTrue(self.chromosome_valid.fitness() < self.chromosome_invalid.fitness())
    
    def test_crossover(self):
        x, y = self.chromosome_valid.crossover(self.chromosome_invalid)
        self.assertIsInstance(x, Chromosome)
        self.assertIsInstance(y, Chromosome)
    
    def test_mutate(self):
        initial_values = self.chromosome_valid.get_colouring().values()
        self.chromosome_valid.mutate(probability=100, colour_set=[i for i in range(1, 61)])
        new_values = self.chromosome_valid.get_colouring().values()
        self.assertCountEqual(initial_values, new_values)
        self.assertNotEqual(new_values, initial_values)
