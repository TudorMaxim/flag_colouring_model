import sys
from PyQt5.QtWidgets import QApplication
from views.home.HomeWidget import HomeWidget


def main():
    app = QApplication(sys.argv)
    home_widget = HomeWidget()
    home_widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
