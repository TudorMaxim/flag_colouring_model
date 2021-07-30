import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from views.home.HomeWidget import HomeWidget
from views.simulator.SimulatorWidget import SimulatorWidget

def main():
    app = QApplication(sys.argv)
    # home_widget = HomeWidget()
    # home_widget.show()
    simulator = SimulatorWidget(parent=None, flags=Qt.WindowFlags())
    simulator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
