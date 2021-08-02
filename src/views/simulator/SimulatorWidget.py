from typing import Optional, Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget
from views.configuration_form.ConfigurationFormWidget import ConfigurationFormWidget
from views.dataset.DatasetWidget import DatasetWidget
from views.home.HomeWidget import HomeWidget
from views.simulator.SimulatorUI import Ui_Simulator
from views.timetable.TimetableWidget import TimetableWidget


class SimulatorWidget(QMainWindow):
    def __init__(self, parent: Optional[QWidget], flags: Union[Qt.WindowFlags, Qt.WindowType]) -> None:
        super().__init__(parent=parent, flags=flags)
        self.ui = Ui_Simulator()
        self.ui.setupUi(self)

        self.home_widget = HomeWidget(parent=self, navigation_callback=self.on_dataset_click)
        self.run_widget = ConfigurationFormWidget(parent=self)
        self.dataset_widget = DatasetWidget(parent=self)
        self.timetable_widget = TimetableWidget(parent=self)

        # Clear the stack widget.
        [self.ui.stacked_widget.removeWidget(self.ui.stacked_widget.widget(0)) for _ in range(2)]

        self.ui.stacked_widget.addWidget(self.home_widget)
        self.ui.stacked_widget.addWidget(self.run_widget)
        self.ui.stacked_widget.addWidget(self.dataset_widget)
        self.ui.stacked_widget.addWidget(self.timetable_widget)
        self.ui.stacked_widget.setCurrentIndex(2)

        self.ui.action_change_dataset.setShortcut('Ctrl+E')
        self.ui.action_change_dataset.triggered.connect(self.on_change_dataset_click)

        self.ui.action_create_timetable.setShortcut('Ctrl+R')
        self.ui.action_create_timetable.triggered.connect(self.on_create_timetable_click)
        
        self.ui.action_dataset.setShortcut('Ctrl+D')
        self.ui.action_dataset.triggered.connect(self.on_dataset_click)

        self.ui.action_timetable.setShortcut('Ctrl+T')
        self.ui.action_timetable.triggered.connect(self.on_timetable_click)

    def on_change_dataset_click(self):
        self.ui.stacked_widget.setCurrentIndex(0)

    def on_create_timetable_click(self):
        self.ui.stacked_widget.setCurrentIndex(1)

    def on_dataset_click(self):
        self.ui.stacked_widget.setCurrentIndex(2)
    
    def on_timetable_click(self):
        self.ui.stacked_widget.setCurrentIndex(3)