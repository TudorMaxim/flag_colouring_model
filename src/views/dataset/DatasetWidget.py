from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from typing import List, Callable
from views.dataset.DatasetUI import Ui_Dataset
from controller.StudentsController import StudentsController
from controller.TeachersController import TeachersController
from model.Teacher import Teacher
from model.Student import Student
from utils import Constants

active_button = 'QPushButton {color: white; background-color: red;}'
inactive_button = 'QPushButton {color: red; background-color: #D3D3D3;}'

class DatasetWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui = Ui_Dataset()
        self.ui.setupUi(self)
        self.dataset = Constants.DEFAULT_DATASET
        self.students_controller = StudentsController(dataset=self.dataset)
        self.teachers_controller = TeachersController(dataset=self.dataset)

        self.ui.students_button.clicked.connect(self.__on_students_button_click)
        self.ui.teachers_button.clicked.connect(self.__on_teachers_button_click)
        self.ui.courses_button.clicked.connect(self.__on_courses_button_click)

        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__populate(
            entities=self.students_controller.get_list(),
            mapper=self.__map_student_to_list_item
        )

    def __populate(self, entities: List, mapper: Callable):
        items = list(map(mapper, entities))
        self.ui.list_widget.clear()
        for item in items:
            self.ui.list_widget.addItem(item)

    def __on_students_button_click(self):
        self.ui.courses_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(active_button)
        self.__populate(
            entities=self.students_controller.get_list(),
            mapper=self.__map_student_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
    
    def __on_teachers_button_click(self):
        self.ui.courses_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(active_button)
        self.__populate(
            entities=self.teachers_controller.get_list(),
            mapper=self.__map_teacher_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_teacher_click)

    def __on_courses_button_click(self):
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.courses_button.setStyleSheet(active_button)
        self.__populate( # TODO: add mapper and on_click event for courses
            entities=[],
            mapper=self.__map_student_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_course_click)

    def __map_student_to_list_item(self, student: Student) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(student.name)
        item.setData(Qt.UserRole, student)
        return item

    def __map_teacher_to_list_item(self, teacher: Teacher) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setText(teacher.name)
        item.setData(Qt.UserRole, teacher)
        return item

    def __on_student_click(self, item: QListWidgetItem) -> None:
        print(item.text())

    def __on_teacher_click(self, item: QListWidgetItem) -> None:
        print(item.text())

    def __on_course_click(self, item: QListWidgetItem) -> None:
        print(item.text())
