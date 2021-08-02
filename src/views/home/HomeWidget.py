from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from views.home.HomeUI import Ui_Home


class HomeWidget(QWidget):
    def __init__(self, parent=None, navigation_callback=None):
        super(HomeWidget, self).__init__(parent=parent)
        self.ui = Ui_Home()
        self.ui.setupUi(self)
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error: Invalid Dataset!")
            msg.setInformativeText('Please select a valid JSON dataset using the BROWSE button.')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.__navigation_callback()