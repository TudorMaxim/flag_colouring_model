from typing import  Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QWidget, QListWidgetItem
from controller.ApplicationController import ApplicationController
from controller.TimetablingController import TimetablingController
from views.timetable.TimetableUI import Ui_Timetable
from utils.Helpers import Helpers


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
        self.ui.export_button.clicked.connect(self.on_export_button_click)

        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.students_repository.get_list(),
            mapper=Helpers.map_student_to_list_item
        )

    def on_export_button_click(self):
        if self.timetabling_controller.colouring is None:
            Helpers.show_error_message(
                message='Error: Could not export the timetable!',
                informative_text='Please create the timetable before trying to export it.'
            )
            return
        try:
            self.ui.export_button.setEnabled(False)
            path = QFileDialog.getSaveFileName(self, 'Save Timetable', '*.csv')
            self.timetabling_controller.export_to_csv(path=path[0])
            self.ui.export_button.setEnabled(True)
        except FileNotFoundError:
            self.ui.export_button.setEnabled(True)

    def on_students_button_click(self):
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(active_button)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_students().values(),
            mapper=Helpers.map_student_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__clear_timetable_widget()

    def on_teachers_button_click(self):
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(active_button)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_teachers().values(),
            mapper=Helpers.map_teacher_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_teacher_click)
        self.__clear_timetable_widget()

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
