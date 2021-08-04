from PyQt5.QtCore import QRunnable
from workers.WorkerSignals import WorkerSignals
from controller.TimetablingController import TimetablingController


class TimetablingWorker(QRunnable):
    def __init__(self, timetabling_controller: TimetablingController) -> None:
        super(TimetablingWorker, self).__init__()
        self.timetabling_controller = timetabling_controller
        self.signals = WorkerSignals()
    
    def run(self) -> None:
        self.signals.runnning.emit()
        try:
            self.timetabling_controller.schedule()
            self.signals.finished.emit()
        except:
            self.signals.error.emit()
