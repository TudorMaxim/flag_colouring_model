# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\views\simulator\Simulator.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Simulator(object):
    def setupUi(self, Simulator):
        Simulator.setObjectName("Simulator")
        Simulator.resize(1226, 758)
        Simulator.setStyleSheet("QWidget#centralwidget {\n"
"    background-color: white;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(Simulator)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo_image = QtWidgets.QLabel(self.centralwidget)
        self.logo_image.setMaximumSize(QtCore.QSize(150, 125))
        self.logo_image.setText("")
        self.logo_image.setPixmap(QtGui.QPixmap(".\\src\\views\\simulator\\../../../assets/klc_logo.svg"))
        self.logo_image.setScaledContents(True)
        self.logo_image.setObjectName("logo_image")
        self.horizontalLayout.addWidget(self.logo_image)
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setStyleSheet("QLabel {\n"
"    font-size: 35px;\n"
"    font-weight: bold;\n"
"    color: red;\n"
"    max-height: 100px;\n"
"}")
        self.title_label.setScaledContents(False)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.horizontalLayout.addWidget(self.title_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget.setObjectName("stacked_widget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stacked_widget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stacked_widget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stacked_widget)
        Simulator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Simulator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1226, 26))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_view = QtWidgets.QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        Simulator.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Simulator)
        self.statusbar.setObjectName("statusbar")
        Simulator.setStatusBar(self.statusbar)
        self.action_change_dataset = QtWidgets.QAction(Simulator)
        self.action_change_dataset.setObjectName("action_change_dataset")
        self.action_dataset = QtWidgets.QAction(Simulator)
        self.action_dataset.setObjectName("action_dataset")
        self.action_timetable = QtWidgets.QAction(Simulator)
        self.action_timetable.setObjectName("action_timetable")
        self.action_create_timetable = QtWidgets.QAction(Simulator)
        self.action_create_timetable.setObjectName("action_create_timetable")
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_change_dataset)
        self.menu_file.addAction(self.action_create_timetable)
        self.menu_view.addAction(self.action_dataset)
        self.menu_view.addAction(self.action_timetable)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())

        self.retranslateUi(Simulator)
        QtCore.QMetaObject.connectSlotsByName(Simulator)

    def retranslateUi(self, Simulator):
        _translate = QtCore.QCoreApplication.translate
        Simulator.setWindowTitle(_translate("Simulator", "University Timetabling Simulator"))
        self.title_label.setText(_translate("Simulator", "University Timetabling Simulator"))
        self.menu_file.setTitle(_translate("Simulator", "&File"))
        self.menu_view.setTitle(_translate("Simulator", "&View"))
        self.action_change_dataset.setText(_translate("Simulator", "Change Dataset"))
        self.action_dataset.setText(_translate("Simulator", "Dataset"))
        self.action_timetable.setText(_translate("Simulator", "Timetable"))
        self.action_create_timetable.setText(_translate("Simulator", "Create Timetable"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Simulator = QtWidgets.QMainWindow()
    ui = Ui_Simulator()
    ui.setupUi(Simulator)
    Simulator.show()
    sys.exit(app.exec_())
