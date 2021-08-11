# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\views\generator\Generator.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Generator(object):
    def setupUi(self, Generator):
        Generator.setObjectName("Generator")
        Generator.resize(871, 240)
        Generator.setStyleSheet("QWidget#Generator {\n"
"    background-color: white;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: red;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton {\n"
"    min-width: 100px;\n"
"    min-height: 35px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    background-color: red;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed {\n"
"    background-color: #EC3812;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Generator)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.students_label = QtWidgets.QLabel(Generator)
        self.students_label.setObjectName("students_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.students_label)
        self.teachers_label = QtWidgets.QLabel(Generator)
        self.teachers_label.setObjectName("teachers_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.teachers_label)
        self.courses_label = QtWidgets.QLabel(Generator)
        self.courses_label.setObjectName("courses_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.courses_label)
        self.min_enrolment_label = QtWidgets.QLabel(Generator)
        self.min_enrolment_label.setObjectName("min_enrolment_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.min_enrolment_label)
        self.max_enrolment_label = QtWidgets.QLabel(Generator)
        self.max_enrolment_label.setObjectName("max_enrolment_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.max_enrolment_label)
        self.students_input = QtWidgets.QLineEdit(Generator)
        self.students_input.setObjectName("students_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.students_input)
        self.teachers_input = QtWidgets.QLineEdit(Generator)
        self.teachers_input.setObjectName("teachers_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.teachers_input)
        self.courses_input = QtWidgets.QLineEdit(Generator)
        self.courses_input.setObjectName("courses_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.courses_input)
        self.min_enrolment_input = QtWidgets.QLineEdit(Generator)
        self.min_enrolment_input.setObjectName("min_enrolment_input")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.min_enrolment_input)
        self.max_entolment_input = QtWidgets.QLineEdit(Generator)
        self.max_entolment_input.setObjectName("max_entolment_input")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.max_entolment_input)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.generate_button = QtWidgets.QPushButton(Generator)
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout.addWidget(self.generate_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(Generator)
        QtCore.QMetaObject.connectSlotsByName(Generator)

    def retranslateUi(self, Generator):
        _translate = QtCore.QCoreApplication.translate
        Generator.setWindowTitle(_translate("Generator", "Form"))
        self.students_label.setText(_translate("Generator", "Students:"))
        self.teachers_label.setText(_translate("Generator", "Teachers:"))
        self.courses_label.setText(_translate("Generator", "Courses:"))
        self.min_enrolment_label.setText(_translate("Generator", "Minimum Enrolment:"))
        self.max_enrolment_label.setText(_translate("Generator", "Maximum Enrolment:"))
        self.generate_button.setText(_translate("Generator", "Generate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Generator = QtWidgets.QWidget()
    ui = Ui_Generator()
    ui.setupUi(Generator)
    Generator.show()
    sys.exit(app.exec_())
