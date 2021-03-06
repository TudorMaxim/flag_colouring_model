from typing import Optional, Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget
from controller.ApplicationController import ApplicationController
from controller.TimetablingController import TimetablingController
from utils import Constants
from views.configuration_form.ConfigurationFormWidget import ConfigurationFormWidget
from views.dataset.DatasetWidget import DatasetWidget
from views.generator.GeneratorWidget import GeneratorWidget
from views.home.HomeWidget import HomeWidget
from views.loader.LoadingSpinnerWidget import LoadingSpinnerWidget
from views.new.CreateEntityWidget import CreateEntityWidget, EntityType
from views.simulator.SimulatorUI import Ui_Simulator
from views.timetable.TimetableWidget import TimetableWidget


class SimulatorWidget(QMainWindow):
    def __init__(self, parent: Optional[QWidget], flags: Union[Qt.WindowFlags, Qt.WindowType]) -> None:
        super().__init__(parent=parent, flags=flags)
        self.ui = Ui_Simulator()
        self.ui.setupUi(self)

        self.application_controller = ApplicationController(dataset_path=Constants.DEFAULT_DATASET)
        self.timetabling_controller = TimetablingController(
            students=self.application_controller.get_students(),
            teachers=self.application_controller.get_teachers(),
            courses=self.application_controller.get_courses()
        )

        self.home_widget = HomeWidget(
            parent=self,
            application_controller=self.application_controller,
            navigation_callback=self.change_dataset
        )
        self.run_widget = ConfigurationFormWidget(
            parent=self,
            timetabling_controller=self.timetabling_controller,
            stacked_widget=self.ui.stacked_widget
        )
        self.dataset_widget = DatasetWidget(
            parent=self,
            application_controller=self.application_controller
        )
        self.timetable_widget = TimetableWidget(
            parent=self,
            application_controller=self.application_controller,
            timetabling_controller=self.timetabling_controller
        )
        self.loader_widget = LoadingSpinnerWidget(parent=self)
        self.generator_widget = GeneratorWidget(
            parent=self,
            application_controller = self.application_controller,
            navigation_callback=self.change_dataset
        )
        self.create_student_widget = CreateEntityWidget(
            parent=self,
            application_controller=self.application_controller,
            type=EntityType.STUDENT,
            navigation_callback=self.on_dataset_click
        )
        self.create_teacher_widget = CreateEntityWidget(
            parent=self,
            application_controller=self.application_controller,
            type=EntityType.TEACHER,
            navigation_callback=self.on_dataset_click
        )
        self.create_course_widget = CreateEntityWidget(
            parent=self,
            application_controller=self.application_controller,
            type=EntityType.COURSE,
            navigation_callback=self.on_dataset_click
        )

        # Clear the stack widget.
        [self.ui.stacked_widget.removeWidget(self.ui.stacked_widget.widget(0)) for _ in range(2)]

        self.ui.stacked_widget.addWidget(self.home_widget)
        self.ui.stacked_widget.addWidget(self.run_widget)
        self.ui.stacked_widget.addWidget(self.dataset_widget)
        self.ui.stacked_widget.addWidget(self.timetable_widget)
        self.ui.stacked_widget.addWidget(self.loader_widget)
        self.ui.stacked_widget.addWidget(self.generator_widget)
        self.ui.stacked_widget.addWidget(self.create_student_widget)
        self.ui.stacked_widget.addWidget(self.create_teacher_widget)
        self.ui.stacked_widget.addWidget(self.create_course_widget)
        self.ui.stacked_widget.setCurrentIndex(2)

        self.ui.action_change_dataset.setShortcut('Ctrl+E')
        self.ui.action_change_dataset.triggered.connect(self.on_change_dataset_click)

        self.ui.create_timetable_action.setShortcut('Ctrl+R')
        self.ui.create_timetable_action.triggered.connect(self.on_create_timetable_click)

        self.ui.create_dataset_action.setShortcut('Ctrl+N')
        self.ui.create_dataset_action.triggered.connect(self.on_create_dataset_click)
        
        self.ui.action_dataset.setShortcut('Ctrl+D')
        self.ui.action_dataset.triggered.connect(self.on_dataset_click)

        self.ui.action_timetable.setShortcut('Ctrl+T')
        self.ui.action_timetable.triggered.connect(self.on_timetable_click)

        self.ui.action_add_student.triggered.connect(self.on_add_student_click)
        self.ui.action_add_teacher.triggered.connect(self.on_add_teacher_click)
        self.ui.action_add_course.triggered.connect(self.on_add_course_click)

    def on_change_dataset_click(self):
        self.ui.stacked_widget.setCurrentIndex(0)

    def on_create_timetable_click(self):
        self.ui.stacked_widget.setCurrentIndex(1)

    def on_create_dataset_click(self):
        self.ui.stacked_widget.setCurrentIndex(5)
    
    def on_add_student_click(self):
        self.create_student_widget.setup()
        self.ui.stacked_widget.setCurrentIndex(6)
    
    def on_add_teacher_click(self):
        self.create_teacher_widget.setup()
        self.ui.stacked_widget.setCurrentIndex(7)
    
    def on_add_course_click(self):
        self.create_course_widget.setup()
        self.ui.stacked_widget.setCurrentIndex(8)
    
    def on_dataset_click(self):
        self.dataset_widget.on_students_button_click()
        self.timetable_widget.on_students_button_click()
        self.ui.stacked_widget.setCurrentIndex(2)
    
    def on_timetable_click(self):
        self.ui.stacked_widget.setCurrentIndex(3)

    def change_dataset(self) -> None:
        self.dataset_widget.on_students_button_click()
        self.timetable_widget.on_students_button_click()
        self.timetabling_controller = TimetablingController(
            students=self.application_controller.get_students(),
            teachers=self.application_controller.get_teachers(),
            courses=self.application_controller.get_courses()
        )
        self.run_widget.timetabling_controller = self.timetabling_controller
        self.timetable_widget.timetabling_controller = self.timetabling_controller
        self.ui.stacked_widget.setCurrentIndex(2)
