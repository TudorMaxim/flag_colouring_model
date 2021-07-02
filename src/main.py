import argparse
from datetime import datetime
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from utils.Conflicts import Conflicts
from algorithms.DegreeOfSaturation import DegreeOfSaturation
from algorithms.LargestDegreeOrdering import LargestDegreeOrdering
from algorithms.RecursiveLargestFirst import RecursiveLargestFirst
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
    args = parser.parse_args()

    students = Student.from_json(args.dataset)
    teachers = Teacher.from_json(args.dataset)
    courses = Course.build_ids_map(Course.from_json(args.dataset))
    conflict_graph = Conflicts.build_graph(students, teachers)
    
    print("CONFLICT GRAPH:")
    print(conflict_graph.adjacency_list)

    options = {
        'ldo': LargestDegreeOrdering,
        'dsatur': DegreeOfSaturation,
        'rlf': RecursiveLargestFirst,
        'ea': EvolutionaryAlgorithm
    }
    colouring_algorithm = options.get(args.algorithm)(conflict_graph)
    colours_set = [i for i in range(1, 61)]
    start_time = datetime.now()
    colouring = colouring_algorithm.run(colours_set)
    elapsed = datetime.now() - start_time

    print("\nTIMETABLE:")
    used_colours_cnt = 0
    for course in colouring:
        print(f'{course}: Colour#{colouring[course]}')
        used_colours_cnt = max(used_colours_cnt, colouring[course])
    print(f'Used colours: {used_colours_cnt}')
    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
