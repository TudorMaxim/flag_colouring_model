import argparse
import json
from utils.Helpers import Helpers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--students', '-s', default=12, help='The number of students from the dataset.')
    parser.add_argument('--teachers', '-t', default=3, help='The number of teachers from the dataset.')
    parser.add_argument('--courses', '-c', default=8, help='The number of courses from the dataset.')
    parser.add_argument('--min_enrolment', '-m', default=1, help='The minimum number of courses a student/teacher can attend/teach.')
    parser.add_argument('--max_enrolment', '-M', default=5, help='The maximum number of courses a student/teacher can attend/teach.')
    args = parser.parse_args()
    
    c = int(args.courses)
    s = int(args.students)
    t = int(args.teachers)
    
    assert s >= c, 'The number of students should be greater than or equal to the number of courses.'
    assert t <= c, 'The number of teachers should be less than or equal to the number of courses.'
    assert s > t, 'The number of students must be greater than the number of teachers.'

    print('Generating dataset with: ')
    print(f'* {c} courses')
    print(f'* {s} students')
    print(f'* {t} teachers')

    print('Generating entities:')
    courses = Helpers.generate_entities(c, default_names=[
        'Big Data Technologies',
        'Model Driven Development',
        'Software Engineering',
        'Distributed Ledgers',
        'Security Engineering',
        'Security Management',
        'Software Testing',
        'Artificial Intelligence'
    ])
    students = Helpers.generate_entities(s, default_names=[
        'Tudor Maxim',
        'Jon Doe',
        'Jane Doe',
        'Mark Doe',
        'Mary Doe'
    ])
    teachers = Helpers.generate_entities(t, default_names=[
        'Jon Smith',
        'Jane Smith',
        'Mark Smith'
    ])
    print('Done!\n')
    minn = int(args.min_enrolment)
    maxx = int(args.max_enrolment)

    teachers = Helpers.assign_courses_to_teachers(teachers, c, t)
    teachers = Helpers.generate_weights(teachers)
    students = Helpers.assign_courses_to_students(students, c, minn, maxx)

    for i in range(len(courses)):
        courses[i]['teacher_id'] = Helpers.find_teacher_id(teachers, courses[i]['id'])
    
    dataset = {
        'courses': courses,
        'teachers': teachers,
        'students': students
    }

    filename = f'dataset_c{c}_s{s}_t{t}.json'
    path = f'./datasets/{filename}'
    print(f'\nWriting file {filename}')
    with open(path, 'w') as file:
        json.dump(dataset, file, indent=4)
    print('\nDataset generated successfully!')



    
