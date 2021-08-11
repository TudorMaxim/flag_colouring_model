from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from controller.ApplicationController import ApplicationController
from model.Course import Course
from utils.Helpers import Helpers
from views.assignment.AssignmentWidget import AssignmentWidget
from views.dataset.DatasetUI import Ui_Dataset
from model.Teacher import Teacher

active_button = 'QPushButton {color: white; background-color: red;}'
inactive_button = 'QPushButton {color: red; background-color: #D3D3D3;}'

class DatasetWidget(QWidget):
    def __init__(self, parent, application_controller: ApplicationController):
        super().__init__(parent=parent)
        self.ui = Ui_Dataset()
        self.ui.setupUi(self)

        self.application_controller = application_controller
        self.can_edit = False
        self.assignment_widget = None

        self.ui.id_input.setEnabled(self.can_edit)
        self.ui.name_input.setEnabled(self.can_edit)
        self.ui.edit_button.clicked.connect(self.__on_edit)
        self.ui.delete_button.clicked.connect(self.__on_delete)

        self.ui.students_button.clicked.connect(self.on_students_button_click)
        self.ui.teachers_button.clicked.connect(self.on_teachers_button_click)
        self.ui.courses_button.clicked.connect(self.on_courses_button_click)
        self.ui.save_dataset_button.clicked.connect(self.on_save_button_click)

        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.ui.list_widget.itemDoubleClicked.connect(self.__on_item_double_click)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_students().values(),
            mapper=Helpers.map_student_to_list_item
        )

    def on_save_button_click(self):
        dataset = self.application_controller.get_dataset()
        self.application_controller.save_dataset(dataset=dataset, path=self.application_controller.dataset_path)
        
    def on_students_button_click(self):
        self.ui.courses_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(active_button)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_students().values(),
            mapper=Helpers.map_student_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_student_click)
        self.__clear_details_page()
        self.ui.courses_list_label.setText('Courses:')
    
    def on_teachers_button_click(self):
        self.ui.courses_button.setStyleSheet(inactive_button)
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(active_button)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_teachers().values(),
            mapper=Helpers.map_teacher_to_list_item
        )
        self.ui.list_widget.itemClicked.disconnect()
        self.ui.list_widget.itemClicked.connect(self.__on_teacher_click)
        self.__clear_details_page()
        self.ui.courses_list_label.setText('Courses:')

    def on_courses_button_click(self):
        self.ui.students_button.setStyleSheet(inactive_button)
        self.ui.teachers_button.setStyleSheet(inactive_button)
        self.ui.courses_button.setStyleSheet(active_button)
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=self.application_controller.get_courses().values(),
            mapper=Helpers.map_course_to_list_item
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
        Helpers.populate(
            list_widget=self.ui.courses_list_widget,
            entities=courses.values(),
            mapper=Helpers.map_course_to_list_item
        )

    def __on_teacher_click(self, item: QListWidgetItem) -> None:
        teacher = item.data(Qt.UserRole)
        self.current_item = teacher
        self.ui.id_input.setText(str(teacher.id))
        self.ui.name_input.setText(teacher.name)
        courses = self.application_controller.get_courses_for(person=teacher)
        self.ui.courses_list_label.setText('Courses:')
        if len(courses):
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=courses.values(),
                mapper=Helpers.map_course_to_list_item
            )
        else:
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=['No course was assigned to this teacher!'],
                mapper=lambda x: QListWidgetItem(x)
            )
        
    def __on_course_click(self, item: QListWidgetItem) -> None:
        course = item.data(Qt.UserRole)
        self.current_item = course
        self.ui.id_input.setText(str(course.id))
        self.ui.name_input.setText(course.name)
        self.ui.courses_list_label.setText('Teacher:')
        teacher = self.application_controller.get_teacher_of(course)
        if teacher is None:
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=['No teacher was assigned to this course!'],
                mapper=lambda x: QListWidgetItem(x)
            )
        else:
            Helpers.populate(
                list_widget=self.ui.courses_list_widget,
                entities=[teacher],
                mapper=Helpers.map_teacher_to_list_item
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
        mapper = Helpers.map_student_to_list_item
        if isinstance(entity, Teacher):
            entities = self.application_controller.get_teachers().values()
            mapper = Helpers.map_teacher_to_list_item
        elif isinstance(entity, Course):
            entities = self.application_controller.get_courses().values()
            mapper = Helpers.map_course_to_list_item
        Helpers.populate(
            list_widget=self.ui.list_widget,
            entities=entities,
            mapper=mapper
        )
        self.__clear_details_page()

    def __clear_details_page(self) -> None:
        self.ui.id_input.setText('')
        self.ui.name_input.setText('')
        self.ui.courses_list_widget.clear()
    
    # Course and teacher assignment
    def __on_item_double_click(self, item):
        entity = item.data(Qt.UserRole)
        navigation_callback = self.on_students_button_click
        if isinstance(entity, Teacher):
            navigation_callback = self.on_teachers_button_click
        elif isinstance(entity, Course):
            navigation_callback = self.on_courses_button_click
        self.assignment_widget = AssignmentWidget(
            parent=None,
            application_controller=self.application_controller,
            entity=entity,
            navigation_callback=navigation_callback
        )
        self.assignment_widget.show()