from PyQt5.QtWidgets import QListWidgetItem, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt
from utils.Helpers import Helpers
from views.assignment.AssignmentUI import Ui_Assignment
from controller.ApplicationController import ApplicationController
from model.Student import Student
from model.Teacher import Teacher
from model.Course import Course
from typing import Callable, List


class AssignmentWidget(QWidget):
    def __init__(
        self, 
        parent=None,
        application_controller: ApplicationController=None,
        entity=None,
        navigation_callback: Callable=None
    ) -> None:
        super().__init__(parent=parent)
        self.ui = Ui_Assignment()
        self.ui.setupUi(self)

        self.application_controller = application_controller
        self.entity = entity
        self.navigation_callback = navigation_callback

        self.ui.save_button.clicked.connect(self.__on_save_button_click)
        self.setup()

    def setup(self) -> None:
        if isinstance(self.entity, Student):
            self.setWindowTitle('Course Assignment for Students')
            self.ui.title_label.setText(f'Assign courses to student {self.entity.name}:')
            self.ui.available_course_label.setText('Courses:')
            self.ui.courses_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=list(filter(lambda c: c.id not in self.entity.course_ids, self.application_controller.get_courses().values())),
                mapper=Helpers.map_course_to_list_item
            )
        elif isinstance(self.entity, Teacher):
            self.setWindowTitle('Course Assignment for Teachers')
            self.ui.title_label.setText(f'Assign courses to teacher {self.entity.name}:')
            self.ui.available_course_label.setText('Courses:')
            self.ui.courses_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=list(filter(
                    lambda c: c.id not in self.entity.course_ids and c.teacher_id is None,
                    self.application_controller.get_courses().values()
                )),
                mapper=Helpers.map_course_to_list_item
            )
        elif isinstance(self.entity, Course):
            self.setWindowTitle('Teacher Assignment for Courses')
            self.ui.title_label.setText(f'Assign teacher to course {self.entity.name}:')
            self.ui.available_course_label.setText('Teachers:')
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=list(filter(lambda t: len(t.course_ids) == 0, self.application_controller.get_teachers().values())),
                mapper=Helpers.map_teacher_to_list_item
            )

    def __on_save_button_click(self) -> None:
        items = self.ui.courses_list_widget.selectedItems()
        self.__assign(items)
        self.navigation_callback()
        self.hide()
    
    def __assign(self, items: List[QListWidgetItem]) -> None:
        if len(items) == 0:
            return
        if isinstance(self.entity, Student):
            courses = list(map(lambda item: item.data(Qt.UserRole), items))
            self.application_controller.assign_courses_to_student(student=self.entity, courses=courses)
        elif isinstance(self.entity, Teacher):
            courses = list(map(lambda item: item.data(Qt.UserRole), items))
            self.application_controller.assign_courses_to_teacher(teacher=self.entity, courses=courses)
        elif isinstance(self.entity, Course):
            teacher = items[0].data(Qt.UserRole)
            self.application_controller.assign_teacher_to_course(course=self.entity, teacher=teacher) 

