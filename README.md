## Flag Colouring Model

### Introduction

This project serves as my dissertation for my master's degree at King's College London. It implements heuristic algorithms and a genetic algorithm to solve the university timetabling problem using graph colouring. The genetic algorithm is designed to improve the solutions found by well-known algorithms like LDO, DSATUR and RLF.

### Deliverables

The software is available in 2 variants:

* CLI - by running the `main.py` file from `src` folder.
* GUI - by running the `app.py` file from `src` folder.

Datasets where generated using `dataset_generator.py` file from `src` folder.

### Code Structure

* The source code is structured in 7 packages under the `src` folder.
* Unit tests are implemented in `tests` folder.

### Instalation

In order to run this project, please install the latest version of Anaconda and Python. After installing Anaconda and cloning the repository, use the following commands:

* `$ cd ./flag_colouring_model` - Naviage in the project's root folder.
* `$ conda env create --prefix env -f flag_colouring_model.yml` - Create the project's environment.
* `$ conda activate ./env` - Activate the project's environment

### GUI Usage

The GUI application can be started using the following command:

* `$ python ./src/app.py`

### CLI Usage
The CLI application can be used with its default settings by executing the following command:

* `$ python ./src/main.py`

The CLI version of this project supports the following arguments:

* `--algorithm`, `-a` – The algorithm to be used when colouring the conflict graph. The accepted values are ldo, dsatur, rlf and ea. The default option is dsatur.
* `--dataset`, `-d` – Path to the dataset JSON file to be loaded into memory and processed.
* `--generations`, `-g` – Number of generations for the evolutionary algorithm. By default, its value is 100.
* `--population`, `-p` – Population size for the evolutionary algorithm. Its default value is 100.
* `--mutation`, `-m` – Mutation rate for the evolutionary algorithm. Its default value is 60%.
* `--model`, `-M` – The population model to be used when executing the evolutionary algorithm. Its possible values are steady_state and generational. By default, the steady-state model is used.
* `--selection`, `-s` – The selection method to be used by the evolutionary algorithm. Its possible values are roulette_wheel and tournament. By default, roulette wheel selection is used.
* `--crossover`, `-c` – The crossover method to be used by the evolutionary algorithm. Its possible values are one_point, two_points and uniform. By default, single point crossover is used.
* `--debug`, `-D` – Boolean argument used to display logs and plot the evolution of the best individual. By default, its value is false.

For example, the following command executes a steady-state evolutionary algorithm using tournament selection and two-points crossover with a mutation probability of 20%, in debug mode:

* `$ python ./src/main.py -a ea -m 20 -M steady_state -s tournament -c two_points -D`

### Generating New Datasets

New datasets can be generated using the `dataset_generator.py` script. It has the following arguments:

* `--students`, `-s` – Number of students to be created.
* `--teachers`, `-t` – Number of teachers to be created.
* `--courses`, `-c` – Number of course to be created.
* `--min_enrolment`, `-m` – Minimum number of courses a student or teacher can attend.
* `--max_enrolment`, `-M` – Maximum number of courses a student or teacher can attend.

For example, a dataset with 20 courses, 100 students and 7 teachers where students mush attend between 2 and 6 courses can be created using the following command:

* `$ python ./src/dataset_generator.py -c 20 -s 100 -t 7 -m 2 -M 6`

