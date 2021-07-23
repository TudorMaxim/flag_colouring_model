import argparse
import json
from typing import List
from random import choice, randint, shuffle

from utils import Constants

# Function that generates n entities based on a list of default names  
def generate_entities(n: int, default_names: List[str]) -> List:
    cnt = [1 for _ in range(len(default_names))]
    entities = []
    for id in range(1, n + 1):
        index = randint(0, len(default_names) - 1)
        name = default_names[index] + f'#{cnt[index]}'
        cnt[index] += 1
        entities.append({
            'id': id, 
            'name': name
        })
    return entities


# Function that randomly assings courses to students
# A student may have many courses and a course may have many students
def assign_courses_to_students(students: List, c: int, minn: int, maxx: int) -> List:
    print('Assigning courses to students:')
    course_ids = [i + 1 for i in range(c)]
    assignments = []
    for student in students:
        shuffle(course_ids)
        cnt = randint(minn, min(c - 1, maxx))
        assignments.append({
            'id': student['id'],
            'name': student['name'],
            'course_ids': course_ids[0:cnt]
        })
    print('Done!\n')
    return assignments


# Function that randomly assigns courses to teachers
# A teacher can have multiple courses, but a course can be held only by one teacher
def assign_courses_to_teachers(teachers: List, c: int, t: int) -> List:
    print('Assigning courses to teachers:')
    course_ids = [i + 1 for i in range(c)]
    shuffle(course_ids)
    for i in range(c):
        idx = i % t 
        if 'course_ids' in teachers[idx]:
            teachers[idx]['course_ids'].append(course_ids[i])
        else:
            teachers[idx]['course_ids'] = [course_ids[i]]
    print('Done!\n')
    return teachers

# Function that finds the id of the teacher who is responsible with a course.
def find_teacher_id(teachers: List, course_id: int) -> int:
    for teacher in teachers:
        if course_id in teacher['course_ids']:
            return teacher['id']
    raise ValueError(f'Error: Could not find a teacher for course with id {course_id}.') 


# Function that randomly generates preferences for teachers.
# 2 - preferred time slot
# 4 - indifferent
# 8 - unpreferred time slot
def generate_weights(teachers: List) -> List:
    print('Generating weights for teachers:')
    options = [2, 4, 8]
    for i in range(len(teachers)):
        # The first element will always be 0 because colours start from 1
        weights = [0] * (Constants.COLOURS_CNT + 1) 
        for j in range(1, len(weights)):
            weights[j] = choice(options)
        teachers[i]['weights'] = weights
    print('Done!\n')
    return teachers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--students', '-s', default=12, help='The number of students from the dataset.')
    parser.add_argument('--teachers', '-t', default=3, help='The number of teachers from the dataset.')
    parser.add_argument('--courses', '-c', default=8, help='The number of courses from the dataset.')
    parser.add_argument('--rooms', '-r', default=8, help='The number of rooms from the dataset.')
    parser.add_argument('--min_enrolment', '-m', default=1, help='The minimum number of courses a student/teacher can attend/teach.')
    parser.add_argument('--max_enrolment', '-M', default=5, help='The maximum number of courses a student/teacher can attend/teach.')
    args = parser.parse_args()
    
    c = int(args.courses)
    s = int(args.students)
    t = int(args.teachers)
    r = int(args.rooms)

    assert(s >= c)
    assert(r <= c)
    assert(t <= c)
    assert(s > t)

    print('Generating dataset with: ')
    print(f'* {c} courses')
    print(f'* {s} students')
    print(f'* {t} teachers')
    print(f'* {r} rooms')

    print('Generating entities:')
    courses = generate_entities(c, default_names=[
        'Big Data Technologies',
        'Model Driven Development',
        'Software Engineering',
        'Distributed Ledgers',
        'Security Engineering',
        'Security Management',
        'Software Testing',
        'Artificial Intelligence'
    ])
    students = generate_entities(s, default_names=[
        'Tudor Maxim',
        'Jon Doe',
        'Jane Doe',
        'Mark Doe',
        'Mary Doe'
    ])
    teachers = generate_entities(t, default_names=[
        'Jon Smith',
        'Jane Smith',
        'Mark Smith'
    ])
    rooms = [{'id': id, 'name': f'Room#{id}'} for id in range(1, r + 1)]
    print('Done!\n')
    minn = int(args.min_enrolment)
    maxx = int(args.max_enrolment)

    teachers = assign_courses_to_teachers(teachers, c, t)
    teachers = generate_weights(teachers)
    students = assign_courses_to_students(students, c, minn, maxx)

    for i in range(len(courses)):
        courses[i]['teacher_id'] = find_teacher_id(teachers, courses[i]['id'])
    
    dataset = {
        'courses': courses,
        'teachers': teachers,
        'students': students,
        'rooms': rooms
    }

    filename = f'dataset_c{c}_s{s}_t{t}_r{r}.json'
    path = f'./datasets/{filename}'
    print(f'\nWriting file {filename}')
    with open(path, 'w') as file:
        json.dump(dataset, file, indent=4)
    print('\nDataset generated successfully!')



    
