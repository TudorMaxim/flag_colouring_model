from model.Student import Student
from model.Teacher import Teacher

if __name__ == '__main__':
    students = Student.from_json()
    for student in students:
        print(student)

    