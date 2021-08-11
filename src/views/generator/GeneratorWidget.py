from typing import Callable
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtGui import QIntValidator
from controller.ApplicationController import ApplicationController
from utils.Helpers import Helpers
from views.generator.GeneratorUI import Ui_Generator

class GeneratorWidget(QWidget):
    def __init__(self, parent, application_controller: ApplicationController, navigation_callback: Callable) -> None:
        super().__init__(parent=parent)
        self.ui = Ui_Generator()
        self.ui.setupUi(self)
        
        self.application_controller = application_controller
        self.navigation_callback = navigation_callback
        
        self.ui.students_input.setText(str(12))
        self.ui.teachers_input.setText(str(3))
        self.ui.courses_input.setText(str(8))
        self.ui.min_enrolment_input.setText(str(1))
        self.ui.max_entolment_input.setText(str(5))

        self.integer_validator = QIntValidator()
        self.setup_integer_validator()

        self.ui.generate_button.clicked.connect(self.generate)

    def generate(self):
        try:
            students = int(self.ui.students_input.text())
            teachers = int(self.ui.teachers_input.text())
            courses = int(self.ui.courses_input.text())
            min_enrolment = int(self.ui.min_enrolment_input.text())
            max_enrolment = int(self.ui.max_entolment_input.text())
            self.ui.generate_button.setEnabled(False)
            dataset = self.application_controller.generate_dataset(
                s=students,
                t=teachers,
                c=courses,
                min_enrolment=min_enrolment,
                max_enrolment=max_enrolment
            )
            path = QFileDialog.getSaveFileName(self, 'Save Dataset', '*.json')
            self.application_controller.save_dataset(dataset, path[0])
            self.application_controller.change_dataset(dataset_path=path[0])
            self.ui.generate_button.setEnabled(True)
            self.navigation_callback()
        except ValueError:
            self.ui.generate_button.setEnabled(True)
            Helpers.show_error_message(
                message='Error: invalid form!',
                informative_text='Please fill in all the inputs or leave the default values.'
            )
        except AssertionError as err:
            self.ui.generate_button.setEnabled(True)
            Helpers.show_error_message(
                message='Error: invalid input',
                informative_text=str(err)
            )
    
    def setup_integer_validator(self):
        integer_inputs = [
            self.ui.students_input, self.ui.teachers_input, self.ui.courses_input,
            self.ui.min_enrolment_input, self.ui.max_entolment_input
        ]
        [integer_input.setValidator(self.integer_validator) for integer_input in integer_inputs]
