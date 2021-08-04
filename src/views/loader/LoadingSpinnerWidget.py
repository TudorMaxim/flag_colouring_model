from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from utils import Constants


class LoadingSpinnerWidget(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        spinner_label = QLabel('Spinner')
        spinner_label.setAlignment(Qt.AlignCenter)
        spinner_movie = QMovie(Constants.LOADING_SPINNER_ANIMATION)
        spinner_label.setMovie(spinner_movie)
        spinner_movie.start()
        layout = QHBoxLayout()
        layout.addWidget(spinner_label)
        self.setLayout(layout)
