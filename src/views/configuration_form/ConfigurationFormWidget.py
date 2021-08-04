from PyQt5.QtWidgets import QWidget
from controller.TimetablingController import TimetablingController
from views.configuration_form.ConfigurationFormUI import Ui_ConfigurationForm


class ConfigurationFormWidget(QWidget):
    def __init__(self, parent,  timetabling_controller: TimetablingController):
        super().__init__(parent=parent,)
        self.ui = Ui_ConfigurationForm()
        self.ui.setupUi(self)
