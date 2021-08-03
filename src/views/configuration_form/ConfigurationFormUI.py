# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\views\configuration_form\ConfigurationForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfigurationForm(object):
    def setupUi(self, ConfigurationForm):
        ConfigurationForm.setObjectName("ConfigurationForm")
        ConfigurationForm.resize(1027, 410)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConfigurationForm.sizePolicy().hasHeightForWidth())
        ConfigurationForm.setSizePolicy(sizePolicy)
        ConfigurationForm.setStyleSheet("QWidget#ConfigurationForm {\n"
"    background: white;\n"
"    /* max-height: 450px; */\n"
"}\n"
"\n"
"QLabel {\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"    qproperty-alignment: AlignLeft;\n"
"    margin-left: 2px;\n"
"}\n"
"\n"
"QToolBox {\n"
"    background-color: white;\n"
"}\n"
"\n"
"QToolBox::tab {\n"
"    font-size: 18px;\n"
"    color: red;\n"
"    font-weight: bold;\n"
"    background-color:     #D3D3D3;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QToolBox::tab:selected {\n"
"    background-color: red;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    max-width: 100px;\n"
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
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfigurationForm)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tool_box = QtWidgets.QToolBox(ConfigurationForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_box.sizePolicy().hasHeightForWidth())
        self.tool_box.setSizePolicy(sizePolicy)
        self.tool_box.setMaximumSize(QtCore.QSize(16777215, 350))
        self.tool_box.setObjectName("tool_box")
        self.algorithm_page = QtWidgets.QWidget()
        self.algorithm_page.setGeometry(QtCore.QRect(0, 0, 1027, 53))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.algorithm_page.sizePolicy().hasHeightForWidth())
        self.algorithm_page.setSizePolicy(sizePolicy)
        self.algorithm_page.setObjectName("algorithm_page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.algorithm_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_form_layout = QtWidgets.QFormLayout()
        self.main_form_layout.setObjectName("main_form_layout")
        self.algorithm_label = QtWidgets.QLabel(self.algorithm_page)
        self.algorithm_label.setStyleSheet("")
        self.algorithm_label.setObjectName("algorithm_label")
        self.main_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.algorithm_label)
        self.algorithm_combo_box = QtWidgets.QComboBox(self.algorithm_page)
        self.algorithm_combo_box.setObjectName("algorithm_combo_box")
        self.algorithm_combo_box.addItem("")
        self.algorithm_combo_box.addItem("")
        self.algorithm_combo_box.addItem("")
        self.algorithm_combo_box.addItem("")
        self.main_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.algorithm_combo_box)
        self.verticalLayout_2.addLayout(self.main_form_layout)
        self.tool_box.addItem(self.algorithm_page, "")
        self.advanced_page = QtWidgets.QWidget()
        self.advanced_page.setGeometry(QtCore.QRect(0, 0, 1027, 162))
        self.advanced_page.setObjectName("advanced_page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.advanced_page)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.genrations_label = QtWidgets.QLabel(self.advanced_page)
        self.genrations_label.setObjectName("genrations_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.genrations_label)
        self.generations_input = QtWidgets.QLineEdit(self.advanced_page)
        self.generations_input.setObjectName("generations_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.generations_input)
        self.population_size_label = QtWidgets.QLabel(self.advanced_page)
        self.population_size_label.setObjectName("population_size_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.population_size_label)
        self.population_size_input = QtWidgets.QLineEdit(self.advanced_page)
        self.population_size_input.setObjectName("population_size_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.population_size_input)
        self.mutation_rate_label = QtWidgets.QLabel(self.advanced_page)
        self.mutation_rate_label.setObjectName("mutation_rate_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.mutation_rate_label)
        self.mutation_rate_input = QtWidgets.QLineEdit(self.advanced_page)
        self.mutation_rate_input.setObjectName("mutation_rate_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.mutation_rate_input)
        self.max_courses_per_day_label = QtWidgets.QLabel(self.advanced_page)
        self.max_courses_per_day_label.setObjectName("max_courses_per_day_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.max_courses_per_day_label)
        self.max_courses_per_day_input = QtWidgets.QLineEdit(self.advanced_page)
        self.max_courses_per_day_input.setObjectName("max_courses_per_day_input")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.max_courses_per_day_input)
        self.max_daily_break_label = QtWidgets.QLabel(self.advanced_page)
        self.max_daily_break_label.setObjectName("max_daily_break_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.max_daily_break_label)
        self.max_daily_break_input = QtWidgets.QLineEdit(self.advanced_page)
        self.max_daily_break_input.setObjectName("max_daily_break_input")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.max_daily_break_input)
        self.horizontalLayout.addLayout(self.formLayout)
        self.tool_box.addItem(self.advanced_page, "")
        self.penalties_page = QtWidgets.QWidget()
        self.penalties_page.setGeometry(QtCore.QRect(0, 0, 1027, 133))
        self.penalties_page.setMaximumSize(QtCore.QSize(16777215, 200))
        self.penalties_page.setObjectName("penalties_page")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.penalties_page)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.invalid_solution_label = QtWidgets.QLabel(self.penalties_page)
        self.invalid_solution_label.setObjectName("invalid_solution_label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.invalid_solution_label)
        self.invalid_solution_input = QtWidgets.QLineEdit(self.penalties_page)
        self.invalid_solution_input.setObjectName("invalid_solution_input")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.invalid_solution_input)
        self.overcrowding_label = QtWidgets.QLabel(self.penalties_page)
        self.overcrowding_label.setObjectName("overcrowding_label")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.overcrowding_label)
        self.overcrowding_input = QtWidgets.QLineEdit(self.penalties_page)
        self.overcrowding_input.setObjectName("overcrowding_input")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.overcrowding_input)
        self.fragmentation_label = QtWidgets.QLabel(self.penalties_page)
        self.fragmentation_label.setObjectName("fragmentation_label")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.fragmentation_label)
        self.fragmentation_input = QtWidgets.QLineEdit(self.penalties_page)
        self.fragmentation_input.setObjectName("fragmentation_input")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.fragmentation_input)
        self.uniformity_label = QtWidgets.QLabel(self.penalties_page)
        self.uniformity_label.setObjectName("uniformity_label")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.uniformity_label)
        self.uniformity_input = QtWidgets.QLineEdit(self.penalties_page)
        self.uniformity_input.setObjectName("uniformity_input")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.uniformity_input)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        self.tool_box.addItem(self.penalties_page, "")
        self.verticalLayout.addWidget(self.tool_box)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.submit_button = QtWidgets.QPushButton(ConfigurationForm)
        self.submit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.submit_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.submit_button.setObjectName("submit_button")
        self.horizontalLayout_2.addWidget(self.submit_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ConfigurationForm)
        self.tool_box.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ConfigurationForm)

    def retranslateUi(self, ConfigurationForm):
        _translate = QtCore.QCoreApplication.translate
        ConfigurationForm.setWindowTitle(_translate("ConfigurationForm", "Form"))
        self.algorithm_label.setText(_translate("ConfigurationForm", "Algorithm:"))
        self.algorithm_combo_box.setItemText(0, _translate("ConfigurationForm", "Largest Degree Ordering Algorithm"))
        self.algorithm_combo_box.setItemText(1, _translate("ConfigurationForm", "Degree Of Saturation Algorithm"))
        self.algorithm_combo_box.setItemText(2, _translate("ConfigurationForm", "Recursive Largest First Algorithm"))
        self.algorithm_combo_box.setItemText(3, _translate("ConfigurationForm", "Evolutionary Algorithm"))
        self.tool_box.setItemText(self.tool_box.indexOf(self.algorithm_page), _translate("ConfigurationForm", "Scheduler"))
        self.genrations_label.setText(_translate("ConfigurationForm", "Generations:"))
        self.generations_input.setText(_translate("ConfigurationForm", "100"))
        self.population_size_label.setText(_translate("ConfigurationForm", "Population Size:"))
        self.population_size_input.setText(_translate("ConfigurationForm", "100"))
        self.mutation_rate_label.setText(_translate("ConfigurationForm", "Mutation Probability:"))
        self.mutation_rate_input.setText(_translate("ConfigurationForm", "60"))
        self.max_courses_per_day_label.setText(_translate("ConfigurationForm", "Max Daily Courses: "))
        self.max_courses_per_day_input.setText(_translate("ConfigurationForm", "6"))
        self.max_daily_break_label.setText(_translate("ConfigurationForm", "Max Daily Break:"))
        self.max_daily_break_input.setText(_translate("ConfigurationForm", "2"))
        self.tool_box.setItemText(self.tool_box.indexOf(self.advanced_page), _translate("ConfigurationForm", "Advanced"))
        self.invalid_solution_label.setText(_translate("ConfigurationForm", "Invalid Solution Penalty:"))
        self.invalid_solution_input.setText(_translate("ConfigurationForm", "1024"))
        self.overcrowding_label.setText(_translate("ConfigurationForm", "Overcrowding Penalty:"))
        self.overcrowding_input.setText(_translate("ConfigurationForm", "64"))
        self.fragmentation_label.setText(_translate("ConfigurationForm", "Fragmentation Penalty:"))
        self.fragmentation_input.setText(_translate("ConfigurationForm", "32"))
        self.uniformity_label.setText(_translate("ConfigurationForm", "Uniformity Penalty:"))
        self.uniformity_input.setText(_translate("ConfigurationForm", "16"))
        self.tool_box.setItemText(self.tool_box.indexOf(self.penalties_page), _translate("ConfigurationForm", "Penalties"))
        self.submit_button.setText(_translate("ConfigurationForm", "Submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigurationForm = QtWidgets.QWidget()
    ui = Ui_ConfigurationForm()
    ui.setupUi(ConfigurationForm)
    ConfigurationForm.show()
    sys.exit(app.exec_())
