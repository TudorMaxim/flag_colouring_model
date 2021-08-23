from argparse import ArgumentParser, BooleanOptionalAction
from datetime import datetime
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from utils import Constants
from utils.Conflicts import Conflicts
from algorithms.DegreeOfSaturation import DegreeOfSaturation
from algorithms.LargestDegreeOrdering import LargestDegreeOrdering
from algorithms.RecursiveLargestFirst import RecursiveLargestFirst
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from algorithms.EvolutionaryAlgorithmConfig import EvolutionaryAlgorithmConfig
from utils.Helpers import Helpers


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        '--algorithm',
        '-a',
        choices=['ldo', 'dsatur', 'rlf', 'ea'],
        default='dsatur',
        help='Algorithm used for colouring the conflict graph.'
    )
    parser.add_argument(
        '--dataset',
        '-d',
        default='./datasets/dataset_c8_s12_t3.json',
        help='Path to the dataset inteded to be used'
    )
    parser.add_argument(
        '--generations',
        '-g',
        default=Constants.GENERATIONS_CNT,
        help='The number of generations when using the evolutionary algorithm. In case of heuristics, this argument is ignored.'
    )
    parser.add_argument(
        '--population',
        '-p',
        default=Constants.POPULATION_CNT,
        help='The size of a population when using the evolutionary algorithm. In case of heuristics, this argument is ignored.'
    )
    parser.add_argument(
        '--mutation',
        '-m',
        default=Constants.MUTATION_PROBABILITY,
        help='The mutation probability when using the evolutionary algorithm. In case of heuristics, this argument is ignored.'
    )
    parser.add_argument(
        '--model',
        '-M',
        default='steady_state',
        choices=['steady_state', 'generational'],
        help='Population model to be used fot the evolutionary algorithm'
    )
    parser.add_argument(
        '--selection',
        '-s',
        default='roulette_wheel',
        choices=['roulette_wheel', 'tournament'],
        help='Selection method to be used for the evolutionary algorithm'
    )
    parser.add_argument(
        '--crossover',
        '-c',
        default='one_point',
        choices=['one_point', 'two_points', 'uniform'],
        help='Crossover method to be used when producing offspring'
    )
    parser.add_argument(
        '--debug',
        '-D',
        default=False,
        action=BooleanOptionalAction,
        help='Debug mode: the evolutionary algorithm will plot its progress.'
    )
    return parser


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()

    print(f'\nParsing dataset {args.dataset}\n')

    students = Helpers.build_ids_map(Student.from_json(args.dataset))
    teachers = Helpers.build_ids_map(Teacher.from_json(args.dataset))
    courses = Helpers.build_ids_map(Course.from_json(args.dataset))
    conflict_graph = Conflicts.build_graph(list(students.values()), list(teachers.values()))
    print(f'Graph Density: {conflict_graph.density()}\n')
    options = {
        'ldo': LargestDegreeOrdering,
        'dsatur': DegreeOfSaturation,
        'rlf': RecursiveLargestFirst,
        'ea': EvolutionaryAlgorithm
    }
    colouring_algorithm = options.get(args.algorithm)(
        graph=conflict_graph,
        students_map=students,
        teachers_map=teachers,
        courses_map=courses
    )
    if isinstance(colouring_algorithm, EvolutionaryAlgorithm):
        colouring_algorithm.generations_cnt = int(args.generations)
        colouring_algorithm.population_cnt = int(args.population)
        colouring_algorithm.mutation_probability = int(args.mutation)
        colouring_algorithm.population_model = EvolutionaryAlgorithmConfig(args.model)
        colouring_algorithm.selection_method = EvolutionaryAlgorithmConfig(args.selection)
        colouring_algorithm.crossover_method = EvolutionaryAlgorithmConfig(args.crossover)
        colouring_algorithm.debug = args.debug
    
    print(f'\nExecuting algorithm: {args.algorithm}\n')

    colours_set = Helpers.generate_colour_set(teachers.values())

    start_time = datetime.now()
    colouring = colouring_algorithm.run(colours_set)
    elapsed = datetime.now() - start_time

    timetable = colouring
    if isinstance(colouring_algorithm, EvolutionaryAlgorithm):
        timetable = colouring[0]
    
    Helpers.print_timetable(courses, timetable)

    print(f'Used colours: {Helpers.get_used_colours_count(timetable)}')

    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
