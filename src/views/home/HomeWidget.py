from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from controller.ApplicationController import ApplicationController
from utils.Helpers import Helpers
from views.home.HomeUI import Ui_Home


class HomeWidget(QWidget):
    def __init__(self, parent=None, application_controller: ApplicationController = None, navigation_callback=None):
        super(HomeWidget, self).__init__(parent=parent)
        self.ui = Ui_Home()
        self.ui.setupUi(self)

        self.application_controller = application_controller
        self.__navigation_callback = navigation_callback

        self.path = ''
        self.ui.selected_dataset_label.setText('')
        self.ui.browse_button.clicked.connect(self.browse)
        self.ui.reset_button.clicked.connect(self.reset)
        self.ui.start_button.clicked.connect(self.start)

    def browse(self):
        self.path = QFileDialog.getOpenFileName(
            self,
            "Select a dataset",
            'E:\\Documents\\Master Kings\\flag_colouring_model\\datasets',
            '*.json'
        )[0]
        self.ui.selected_dataset_label.setText(self.get_dataset_name())
    
    def get_dataset_name(self):
        truncated = self.path.split("/")
        return truncated[-1]

    def reset(self):
        self.path = ''
        self.ui.selected_dataset_label.setText('')
    
    def start(self):
        if self.path == '':
            Helpers.show_error_message(
                message='Error: Invalid Dataset!',
                informative_text='Please select a valid JSON dataset using the BROWSE button.'
            )
        else:
            self.application_controller.change_dataset(self.path)
            self.__navigation_callback()
