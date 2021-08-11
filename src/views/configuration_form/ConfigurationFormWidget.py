from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QStackedWidget, QWidget
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithmConfig
from controller.TimetablingController import TimetablingController
from utils.Helpers import Helpers
from views.configuration_form.ConfigurationFormUI import Ui_ConfigurationForm
from workers.TimetablingWorker import TimetablingWorker


class ConfigurationFormWidget(QWidget):
    def __init__(self, parent, timetabling_controller: TimetablingController, stacked_widget: QStackedWidget):
        super().__init__(parent=parent,)
        self.ui = Ui_ConfigurationForm()
        self.ui.setupUi(self)
        
        self.thread_pool = QThreadPool()
        self.worker = None
        self.timetabling_controller = timetabling_controller
        self.stacked_widget = stacked_widget

        self.ui.algorithm_combo_box.currentIndexChanged.connect(self.on_algorithm_combo_box_change)
        self.toggle_advanced_options(algorithm=str(self.ui.algorithm_combo_box.currentText()))
        
        self.integer_validator = QIntValidator()
        self.setup_integer_validator()
        
        self.ui.submit_button.clicked.connect(self.submit)
        
    def on_algorithm_combo_box_change(self) -> None:
        algorithm = str(self.ui.algorithm_combo_box.currentText())
        self.toggle_advanced_options(algorithm)

    def submit(self) -> None:
        try:
            population_model = EvolutionaryAlgorithmConfig.STEADY_STATE_POPULATION
            if 'Generational' in str(self.ui.population_model_combo_box.currentText()):
                population_model = EvolutionaryAlgorithmConfig.GENERATIONAL_POPULATION
            
            selection_method = EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SELECTION
            if 'Tournament' in str(self.ui.selection_method_combo_box.currentText()):
                selection_method = EvolutionaryAlgorithmConfig.TOURNAMENT_SELECTION
            
            self.timetabling_controller.set_algorithm(
                name=str(self.ui.algorithm_combo_box.currentText()),
                population_cnt=int(self.ui.population_size_input.text()),
                generations_cnt=int(self.ui.generations_input.text()),
                mutation_rate=int(self.ui.mutation_rate_input.text()),
                population_model=population_model,
                selection_method=selection_method

            )
            self.timetabling_controller.set_constants(
                max_courses_per_day=int(self.ui.max_courses_per_day_input.text()),
                max_daily_break=int(self.ui.max_daily_break_input.text())
            )
            self.timetabling_controller.set_penalties(
                invalid_colouring=int(self.ui.invalid_solution_input.text()),
                overcrowding=int(self.ui.overcrowding_input.text()),
                fragmentation=int(self.ui.fragmentation_input.text()),
                uniformity=int(self.ui.uniformity_input.text())
            )

            self.worker = TimetablingWorker(self.timetabling_controller)
            self.worker.signals.runnning.connect(self.running)
            self.worker.signals.finished.connect(self.finished)
            self.worker.signals.error.connect(self.error)
            self.thread_pool.start(self.worker)
        except ValueError:
            Helpers.show_error_message(
                message='Error: invalid form!',
                informative_text='Please fill in all the fields or leave the default values.'
            )

    def running(self) -> None:
        self.stacked_widget.setCurrentIndex(4)

    def finished(self) -> None:
        self.stacked_widget.setCurrentIndex(3)

    def error(self) -> None:
        self.stacked_widget.setCurrentIndex(3)

    def setup_integer_validator(self) -> None:
        integer_inputs = [
            self.ui.generations_input, self.ui.population_size_input, self.ui.mutation_rate_input,
            self.ui.max_courses_per_day_input, self.ui.max_daily_break_input,
            self.ui.invalid_solution_input, self.ui.overcrowding_input,
            self.ui.fragmentation_input, self.ui.uniformity_input,
        ]
        [integer_input.setValidator(self.integer_validator) for integer_input in integer_inputs]
    
    def toggle_advanced_options(self, algorithm: str):
        advanced_inputs = [
            self.ui.selection_method_combo_box, self.ui.population_model_combo_box, 
            self.ui.generations_input, self.ui.population_size_input, self.ui.mutation_rate_input,
            self.ui.max_courses_per_day_input, self.ui.max_daily_break_input, 
            self.ui.invalid_solution_input, self.ui.overcrowding_input,
            self.ui.fragmentation_input, self.ui.uniformity_input
        ]
        if algorithm == 'Evolutionary Algorithm':
            [advanced_input.setEnabled(True) for advanced_input in advanced_inputs]
        else:
            [advanced_input.setEnabled(False) for advanced_input in advanced_inputs]
        
