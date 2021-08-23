import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from views.simulator.SimulatorWidget import SimulatorWidget

def main():
    app = QApplication(sys.argv)
    simulator = SimulatorWidget(parent=None, flags=Qt.WindowFlags())
    simulator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()