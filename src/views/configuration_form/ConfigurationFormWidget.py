from PyQt5.QtWidgets import QWidget
from views.configuration_form.ConfigurationFormUI import Ui_ConfigurationForm


class ConfigurationFormWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui = Ui_ConfigurationForm()
        self.ui.setupUi(self)
