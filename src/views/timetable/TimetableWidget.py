from PyQt5.QtWidgets import QWidget
from views.timetable.TimetableUI import Ui_Timetable


class TimetableWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui = Ui_Timetable()
        self.ui.setupUi(self)
