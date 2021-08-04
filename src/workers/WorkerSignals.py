from PyQt5.QtCore import QObject, pyqtSignal


class WorkerSignals(QObject):
    runnning = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal()
