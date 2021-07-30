from typing import Optional, Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QMainWindow, QWidget
from controller.StudentsController import StudentsController
from controller.TeachersController import TeachersController
from model.Student import Student
from model.Teacher import Teacher
from utils import Constants
from views.simulator.SimulatorUI import Ui_Simulator


class SimulatorWidget(QMainWindow):
    def __init__(self, parent: Optional[QWidget], flags: Union[Qt.WindowFlags, Qt.WindowType]) -> None:
        super().__init__(parent=parent, flags=flags)
        self.ui = Ui_Simulator()
        self.ui.setupUi(self)

        self.dataset = Constants.DEFAULT_DATASET
        self.students_controller = StudentsController(dataset=self.dataset)
        self.teachers_controller = TeachersController(dataset=self.dataset)

        student_items = list(map(self.__map_student_to_list_item, self.students_controller.get_list()))
        self.ui.students_list_widget.itemClicked.connect(self.on_student_click)
        for student in student_items:
            self.ui.students_list_widget.addItem(student)

        teacher_items = list(map(self.__map_teacher_to_list_item, self.teachers_controller.get_list()))
        self.ui.teachers_list_widget.itemClicked.connect(self.on_teacher_click)
        for teacher in teacher_items:
            self.ui.teachers_list_widget.addItem(teacher)
        

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
    
    def on_student_click(self, item: QListWidgetItem) -> None:
        print(item.text())
    
    def on_teacher_click(self, item: QListWidgetItem) -> None:
        print(item.text())
    

