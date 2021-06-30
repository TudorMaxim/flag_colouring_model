import argparse
from datetime import datetime
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from utils.Conflicts import Conflicts
from algorithms.ldo import largest_degree_ordering
from algorithms.dsatur import degree_of_saturation_algorithm
from algorithms.rlf import recursive_largest_first_algorithm
from algorithms.ea import evolutionary_algorithm


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

    switcher = {
        'ldo': largest_degree_ordering,
        'dsatur': degree_of_saturation_algorithm,
        'rlf': recursive_largest_first_algorithm,
        'ea': evolutionary_algorithm
    }
    colouring_algorithm = switcher.get(args.algorithm)

    students = Student.from_json(args.dataset)
    teachers = Teacher.from_json(args.dataset)
    courses = Course.build_ids_map(Course.from_json(args.dataset))
    conflict_graph = Conflicts.build_graph(students, teachers)
    
    print("CONFLICT GRAPH:")
    print(conflict_graph.adjacency_list)

    start_time = datetime.now()
    colouring = colouring_algorithm(conflict_graph)
    elapsed = datetime.now() - start_time

    print("\nTIMETABLE:")
    used_colours_cnt = 0
    for course in colouring:
        print(f'{course}: Colour#{colouring[course]}')
        used_colours_cnt = max(used_colours_cnt, colouring[course])
    print(f'Used colours: {used_colours_cnt}')
    print(f'\n\nElapsed time: {elapsed.total_seconds() * 1000} ms')
