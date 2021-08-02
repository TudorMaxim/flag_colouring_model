# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\views\home\Home.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Home(object):
    def setupUi(self, Home):
        Home.setObjectName("Home")
        Home.resize(1028, 175)
        Home.setStyleSheet("QWidget#Home {\n"
"    background: white;\n"
"    max-height: 175px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: red;\n"
"    font-weight: bold;\n"
"    font-size: 18px;\n"
"    height: 35px;\n"
"}\n"
"\n"
"QLabel#select_label {\n"
"    qproperty-alignment: AlignLeft;\n"
"    margin-top: 24px;\n"
"    margin-bottom: 2px;\n"
"}\n"
"\n"
"QLabel#selected_dataset_label {\n"
"    qproperty-alignment: AlignLeft;\n"
"    padding-top: 5px;\n"
"    border: 1px solid red;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    height: 35px;\n"
"    width: 100px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    background-color: red;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed {\n"
"    background-color: #EC3812;\n"
"}\n"
"\n"
"\n"
"QPushButton#reset_button {\n"
"    max-height: 35px;\n"
"    color: red;\n"
"    font-weight: bold;\n"
"    background-color:     #D3D3D3;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#reset_button:hover:!pressed {\n"
"    background-color: #DCDCDC;\n"
"}\n"
"\n"
"\n"
"")
        self.home_layout = QtWidgets.QVBoxLayout(Home)
        self.home_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.home_layout.setObjectName("home_layout")
        self.selection_vertical_layout = QtWidgets.QVBoxLayout()
        self.selection_vertical_layout.setSpacing(7)
        self.selection_vertical_layout.setObjectName("selection_vertical_layout")
        self.select_label = QtWidgets.QLabel(Home)
        self.select_label.setStyleSheet("")
        self.select_label.setAlignment(QtCore.Qt.AlignLeading)
        self.select_label.setObjectName("select_label")
        self.selection_vertical_layout.addWidget(self.select_label)
        self.selection_horizontal_layout = QtWidgets.QHBoxLayout()
        self.selection_horizontal_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.selection_horizontal_layout.setObjectName("selection_horizontal_layout")
        self.selected_dataset_label = QtWidgets.QLabel(Home)
        self.selected_dataset_label.setStyleSheet("")
        self.selected_dataset_label.setAlignment(QtCore.Qt.AlignLeading)
        self.selected_dataset_label.setObjectName("selected_dataset_label")
        self.selection_horizontal_layout.addWidget(self.selected_dataset_label)
        self.browse_button = QtWidgets.QPushButton(Home)
        self.browse_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browse_button.setStyleSheet("QPushButton {\n"
"    max-width: 100px;\n"
"    max-height: 35px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    background-color: red;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed {\n"
"    background-color: #EC3812;\n"
"}")
        self.browse_button.setCheckable(False)
        self.browse_button.setChecked(False)
        self.browse_button.setFlat(False)
        self.browse_button.setObjectName("browse_button")
        self.selection_horizontal_layout.addWidget(self.browse_button)
        self.selection_vertical_layout.addLayout(self.selection_horizontal_layout)
        self.action_buttons_layout = QtWidgets.QHBoxLayout()
        self.action_buttons_layout.setObjectName("action_buttons_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.action_buttons_layout.addItem(spacerItem)
        self.reset_button = QtWidgets.QPushButton(Home)
        self.reset_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reset_button.setStyleSheet("")
        self.reset_button.setObjectName("reset_button")
        self.action_buttons_layout.addWidget(self.reset_button)
        self.start_button = QtWidgets.QPushButton(Home)
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_button.setStyleSheet("")
        self.start_button.setObjectName("start_button")
        self.action_buttons_layout.addWidget(self.start_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.action_buttons_layout.addItem(spacerItem1)
        self.selection_vertical_layout.addLayout(self.action_buttons_layout)
        self.home_layout.addLayout(self.selection_vertical_layout)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "University Timetabling Simutator"))
        self.select_label.setText(_translate("Home", "Select Dataset:"))
        self.selected_dataset_label.setText(_translate("Home", "small_dataset.json"))
        self.browse_button.setText(_translate("Home", "Browse"))
        self.reset_button.setText(_translate("Home", "Reset"))
        self.start_button.setText(_translate("Home", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Home = QtWidgets.QWidget()
    ui = Ui_Home()
    ui.setupUi(Home)
    Home.show()
    sys.exit(app.exec_())
