from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QListWidget
from typing import List, Callable
from controller.ApplicationController import ApplicationController
from model.Course import Course
from views.dataset.DatasetUI import Ui_Dataset
from model.Teacher import Teacher
from model.Student import Student

active_button = 'QPushButton {color: white; background-color: red;}'
inactive_button = 'QPushButton {color: red; background-color: #D3D3D3;}'

class DatasetWidget(QWidget):
    def __init__(self, parent, application_controller: ApplicationController):
        super().__init__(parent=parent)
        self.ui = Ui_Dataset()
        self.ui.setupUi(self)

        self.application_controller = application_controller
        self.can_edit = False

        self.ui.id_input.setEnabled(self.can_edit)
        self.ui.name_input.setEnabled(self.can_edit)
        self.ui.edit_button.clicked.connect(self.__on_edit)
        self.ui.delete_button.clicked.connect(self.__on_delete)

        self.ui.students_button.clicked.connect(self.on_students_button_click)
        self.ui.teachers_button.clicked.connect(self.on_teachers_button_click)
        self.ui.courses_button.clicked.connect(self.on_courses_button_click)

        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.students_repository.get_list(),
            mapper=self.__map_student_to_list_item
        )

    def __populate(self, list_widget: QListWidget, entities: List, mapper: Callable):
        list_widget.clear()
        items = list(map(mapper, entities))
        for item in items:
            list_widget.addItem(item)

    def on_students_button_click(self):
        self.ui.courses_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(active_button)
        self.__populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_students().values(),
            mapper=self.__map_student_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__clear_details_page()
        self.ui.courses_list_label.setText('Courses:')
    
    def on_teachers_button_click(self):
        self.ui.courses_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(active_button)
        self.__populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_teachers().values(),
            mapper=self.__map_teacher_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_teacher_click)
        self.__clear_details_page()
        self.ui.courses_list_label.setText('Courses:')

    def on_courses_button_click(self):
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.courses_button.setStyleSheet(active_button)
        self.__populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_courses().values(),
            mapper=self.__map_course_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_course_click)
        self.__clear_details_page()
        self.ui.courses_list_label.setText('Teachers:')

    # update details page
    def __on_student_click(self, item: QListWidgetItem) -> None:
        student = item.data(Qt.UserRole)
        self.current_item = student
        self.ui.id_input.setText(str(student.id))
        self.ui.name_input.setText(student.name)
        courses = self.application_controller.get_courses_for(person=student)
        self.ui.courses_list_label.setText('Courses:')
        self.__populate(
            list_widget=self.ui.courses_list_widget,
            entities=courses.values(),
            mapper=self.__map_course_to_list_item
        )

    def __on_teacher_click(self, item: QListWidgetItem) -> None:
        teacher = item.data(Qt.UserRole)
        self.current_item = teacher
        self.ui.id_input.setText(str(teacher.id))
        self.ui.name_input.setText(teacher.name)
        courses = self.application_controller.get_courses_for(person=teacher)
        self.ui.courses_list_label.setText('Courses:')
        self.__populate(
            list_widget=self.ui.courses_list_widget,
            entities=courses.values(),
            mapper=self.__map_course_to_list_item
        )

    def __on_course_click(self, item: QListWidgetItem) -> None:
        course = item.data(Qt.UserRole)
        self.current_item = course
        self.ui.id_input.setText(str(course.id))
        self.ui.name_input.setText(course.name)
        self.ui.courses_list_label.setText('Teacher:')
        teacher = self.application_controller.get_teacher_of(course)
        if teacher is None:
            self.__populate(
                list_widget=self.ui.courses_list_widget,
                entities=['No teacher was assigned to this course'],
                mapper=lambda x: QListWidgetItem(x)
            )
        else:
            self.__populate(
                list_widget=self.ui.courses_list_widget,
                entities=[teacher],
                mapper=self.__map_teacher_to_list_item
            )

    # Details Page actions
    def __on_edit(self):
        item = self.ui.list_widget.currentItem()
        if item is None:
            return
        entity = item.data(Qt.UserRole)
        if self.can_edit:
            name = self.ui.name_input.text()
            self.application_controller.update(entity, name)
            item.setText(name)
            item.setData(Qt.UserRole, entity)
            self.can_edit = False
            self.ui.edit_button.setText('Edit')
        else:
            self.can_edit = True
            self.ui.edit_button.setText('Save')
        self.ui.name_input.setEnabled(self.can_edit)

    def __on_delete(self):
        item = self.ui.list_widget.currentItem()
        if item is None:
            return 
        entity = item.data(Qt.UserRole)
        self.application_controller.delete(entity)
        entities = self.application_controller.get_students().values()
        mapper = self.__map_student_to_list_item
        if isinstance(entity, Teacher):
            entities = self.application_controller.get_teachers().values()
            mapper = self.__map_teacher_to_list_item
        elif isinstance(entity, Course):
            entities = self.application_controller.get_courses().values()
            mapper = self.__map_course_to_list_item
        self.__populate(
            list_widget=self.ui.list_widget,
            entities=entities,
            mapper=mapper
        )
        self.__clear_details_page()

    def __clear_details_page(self) -> None:
        self.ui.id_input.setText('')
        self.ui.name_input.setText('')
        self.ui.courses_list_widget.clear()
    
    # Mappers
    def __map_student_to_list_item(self, student: Student) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(student.name)
        item.setData(Qt.UserRole, student)
        return item

    def __map_course_to_list_item(self, course: Course) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(course.name)
        item.setData(Qt.UserRole, course)
        return item

    def __map_teacher_to_list_item(self, teacher: Teacher) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(teacher.name)
        item.setData(Qt.UserRole, teacher)
        return item
