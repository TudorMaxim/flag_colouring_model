from algorithms.DegreeOfSaturation import DegreeOfSaturation
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm, EvolutionaryAlgorithmConfig
from algorithms.LargestDegreeOrdering import LargestDegreeOrdering
from algorithms.RecursiveLargestFirst import RecursiveLargestFirst
from model.Course import Course
from model.Student import Student
from model.Teacher import Teacher
from utils import Constants
from utils.Conflicts import Conflicts
from utils.Helpers import Helpers


class TimetablingController:
    def __init__(self, students: dict[int, Student], teachers: dict[int, Teacher], courses: dict[int, Course]) -> None:
        self.students = students
        self.teachers = teachers
        self.courses = courses
        self.colour_set = Helpers.generate_colour_set(list(self.teachers.values()))
        self.conflict_graph = Conflicts.build_graph(list(students.values()), list(teachers.values()))
        self.algorithm = LargestDegreeOrdering( # Default Algorithm
            graph=self.conflict_graph,
            students_map=self.students,
            teachers_map=self.teachers,
            courses_map=self.courses
        )
        self.colouring = None

    def set_algorithm(
        self,
        name: str,
        population_cnt: int = 100,
        generations_cnt: int = 100,
        mutation_rate: int = 60,
        population_model: EvolutionaryAlgorithmConfig = EvolutionaryAlgorithmConfig.STEADY_STATE_POPULATION,
        selection_method: EvolutionaryAlgorithmConfig = EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SELECTION
    ) -> None:
        options = {
            'Largest Degree Ordering Algorithm': LargestDegreeOrdering,
            'Degree Of Saturation Algorithm': DegreeOfSaturation,
            'Recursive Largest First Algorithm': RecursiveLargestFirst,
            'Evolutionary Algorithm': EvolutionaryAlgorithm, 
        }
        self.algorithm = options.get(name)(
            graph=self.conflict_graph,
            students_map=self.students,
            teachers_map=self.teachers,
            courses_map=self.courses
        )
        if isinstance(self.algorithm, EvolutionaryAlgorithm):
            self.algorithm.generations_cnt = generations_cnt
            self.algorithm.population_cnt = population_cnt
            self.algorithm.mutation_probability = mutation_rate
            self.algorithm.population_model = population_model
            self.algorithm.selection_method = selection_method
    
    def set_penalties(self, invalid_colouring: int, overcrowding: int, fragmentation: int, uniformity: int) -> None:
        Constants.IVALID_COLOURING_PENALTY = invalid_colouring
        Constants.OVERCROWDING_PENALTY = overcrowding
        Constants.FRAGMENTATION_PENALTY = fragmentation
        Constants.UNIFORMITY_PENALTY = uniformity

    def set_constants(self, max_courses_per_day: int, max_daily_break: int) -> None:
        Constants.MAX_COURSES_PER_DAY = max_courses_per_day
        Constants.MAX_DAILY_BREAK = max_daily_break
    
    def schedule(self) -> dict[int, int]:
        self.colouring = self.algorithm.run(self.colour_set)
        return self.colouring