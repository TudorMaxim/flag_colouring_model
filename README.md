## Flag Colouring Model

### Introduction

This project serves as my dissertation for my master's degree at King's College London. It implements heuristic algorithms to solve the university timetabling problem using graph colouring. Also, a genetic algorithm is designed and implemented to improve the solutions found by algorithms like LDO, DSATUR and RLF.

### Deliverables

The software is available in 2 variants:

* CLI - by running the `main.py` file from `src` folder.
* GUI - by running the `app.py` file from `src` folder.

Datasets where generated using `dataset_generator.py` file from `src` folder.

### Code Structure

* The source code is structured in 7 packages under the `src` folder.
* Unit tests are implemented in `tests` folder.

### Instalation

In order to run this project, please install the latest version of Anaconda and Python. 

After installing Anaconda and cloning the repository, use the following commands:

* `$ cd ./flag_colouring_model` - Naviage in the project's root folder.
* `$ conda env create --prefix env -f flag_colouring_model.yml` - Create the project's environment.
* `$ conda activate ./env` - Activate the project's environment

### Usage

The GUI application can be started using the following command:

* `$ python ./src/app.py`

