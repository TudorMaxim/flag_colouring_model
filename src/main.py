from argparse import ArgumentParser
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
        default='./datasets/small_dataset.json',
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
    return parser


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()

    print(f'\nParsing dataset {args.dataset}\n')

    students = Helpers.build_ids_map(Student.from_json(args.dataset))
    teachers = Helpers.build_ids_map(Teacher.from_json(args.dataset))
    courses = Helpers.build_ids_map(Course.from_json(args.dataset))
    conflict_graph = Conflicts.build_graph(list(students.values()), list(teachers.values()))
    
    # print("CONFLICT GRAPH:")
    # print(conflict_graph.adjacency_list)

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
    
    print(f'\nExecuting algorithm: {args.algorithm}\n')

    colours_set = [i for i in range(1, Constants.COLOURS_CNT + 1)]
    start_time = datetime.now()
    colouring = colouring_algorithm.run(colours_set)
    elapsed = datetime.now() - start_time

    print("TIMETABLE:")
    used_colours_cnt = 0
    for course in colouring:
        print(f'{course}: Colour#{colouring[course]}')
        used_colours_cnt = max(used_colours_cnt, colouring[course])
    # print(f'Used colours: {used_colours_cnt}')
    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
