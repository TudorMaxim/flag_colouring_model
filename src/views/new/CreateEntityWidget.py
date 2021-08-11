from typing import Callable
from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QWidget
from views.new.CreateEntityUI import Ui_CreateEntity
from controller.ApplicationController import ApplicationController
from utils.Helpers import Helpers


class EntityType(Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    COURSE = 'course'

class CreateEntityWidget(QWidget):
    def __init__(self, parent, application_controller: ApplicationController, type: EntityType, navigation_callback: Callable):
        super().__init__(parent=parent)
        self.ui = Ui_CreateEntity()
        self.ui.setupUi(self)

        self.application_controller = application_controller
        self.type = type
        self.navigation_callback = navigation_callback

        self.ui.save_button.clicked.connect(self.on_save_button_click)
        self.setup()
        
    def setup(self):
        self.ui.name_input.setText('')
        if self.type == EntityType.STUDENT:
            self.ui.create_label.setText('Create New Student:')
            self.ui.courses_list_widget.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=self.application_controller.get_courses().values(),
                mapper=Helpers.map_course_to_list_item
            )
        elif self.type == EntityType.TEACHER:
            self.ui.create_label.setText('Create New Teacher:')
            self.ui.courses_list_widget.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=list(filter(lambda c: c.teacher_id is None,
                              self.application_controller.get_courses().values())),
                mapper=Helpers.map_course_to_list_item
            )
        elif self.type == EntityType.COURSE:
            self.ui.create_label.setText('Create New Course')
            self.ui.courses_label.setText('Teachers:')
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=list(filter(lambda t: len(t.course_ids) == 0,
                              self.application_controller.get_teachers().values())),
                mapper=Helpers.map_teacher_to_list_item
            )

    def on_save_button_click(self):
        if self.type == EntityType.STUDENT:
            self.__save_student()
        elif self.type == EntityType.TEACHER:
            self.__save_teacher()
        elif self.type == EntityType.COURSE:
            self.__save_course()

    def __save_student(self):
        name = self.ui.name_input.text()
        items = self.ui.courses_list_widget.selectedItems()
        courses = list(map(lambda item: item.data(Qt.UserRole), items))
        course_ids = list(map(lambda course: course.id, courses))
        try:
            self.application_controller.add_student(name, course_ids)
            self.navigation_callback()
        except AssertionError as err:
            Helpers.show_error_message(
                message='Error: Could not save student!',
                informative_text=str(err)
            )

    def __save_teacher(self):
        name = self.ui.name_input.text()
        items = self.ui.courses_list_widget.selectedItems()
        courses = list(map(lambda item: item.data(Qt.UserRole), items))
        course_ids = list(map(lambda course: course.id, courses))
        try:
            self.application_controller.add_teacher(name, course_ids)
            self.navigation_callback()
        except AssertionError as err:
            Helpers.show_error_message(
                message='Error: Could not save teacher!',
                informative_text=str(err)
            )

    def __save_course(self):
        name = self.ui.name_input.text()
        items = self.ui.courses_list_widget.selectedItems()
        teacher_id = None
        if len(items):
            teacher_id = items[0].data(Qt.UserRole).id
        try:
            self.application_controller.add_course(name, teacher_id)
            self.navigation_callback()
        except AssertionError as err:
            Helpers.show_error_message(
                message='Error: Could not save teacher!',
                informative_text=str(err)
            )
