from typing import List, Callable, Optional
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from controller.ApplicationController import ApplicationController
from controller.TimetablingController import TimetablingController
from utils.Helpers import Helpers
from views.timetable.TimetableUI import Ui_Timetable
from model.Teacher import Teacher
from model.Student import Student


active_button = 'QPushButton {color: white; background-color: red;}'
inactive_button = 'QPushButton {color: red; background-color: #D3D3D3;}'

class TimetableWidget(QWidget):
    def __init__(self, parent, application_controller: ApplicationController, timetabling_controller: TimetablingController):
        super().__init__(parent=parent)
        self.ui = Ui_Timetable()
        self.ui.setupUi(self)

        self.application_controller = application_controller
        self.timetabling_controller = timetabling_controller

        self.ui.students_button.clicked.connect(self.on_students_button_click)
        self.ui.teachers_button.clicked.connect(self.on_teachers_button_click)

        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__populate(
            entities=self.application_controller.students_repository.get_list(),
            mapper=self.__map_student_to_list_item
        )

    def __populate(self, entities: List, mapper: Callable):
        items = list(map(mapper, entities))
        self.ui.list_widget.clear()
        for item in items:
            self.ui.list_widget.addItem(item)

    def on_students_button_click(self):
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(active_button)
        self.__populate(
            entities=self.application_controller.students_repository.get_list(),
            mapper=self.__map_student_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__clear_timetable_widget()

    def on_teachers_button_click(self):
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(active_button)
        self.__populate(
            entities=self.application_controller.teachers_repository.get_list(),
            mapper=self.__map_teacher_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_teacher_click)
        self.__clear_timetable_widget()

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
        student = item.data(Qt.UserRole)
        timetable = self.timetabling_controller.get_student_timetable(student.id)
        self.__populate_timetable_widget(timetable)

    def __on_teacher_click(self, item: QListWidgetItem) -> None:
        teacher = item.data(Qt.UserRole)
        timetable = self.timetabling_controller.get_teacher_timetable(teacher.id)
        self.__populate_timetable_widget(timetable)

    def __populate_timetable_widget(self, timetable: Optional[dict[int, int]]) -> None:
        if not timetable:
            return
        self.__clear_timetable_widget()
        for course_id in timetable:
            colour = timetable[course_id]
            course = self.application_controller.get_course(course_id)
            item = QTableWidgetItem()
            item.setText(course.name)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(Qt.red)
            item.setForeground(Qt.white)
            hour, day = Helpers.get_hour_and_day(colour)
            self.ui.timetable_widget.setItem(hour, day, item)
        
    def __clear_timetable_widget(self):
        for i in range(12):
            for j in range(5):
                self.ui.timetable_widget.setItem(i, j, QTableWidgetItem())
