import numpy as np
from typing import List, Tuple
from copy import deepcopy
from random import randint
from model.Course import Course
from model.Graph import Graph
from model.Student import Student
from model.Teacher import Teacher
from utils import Constants


class Chromosome:
    def __init__(
        self, graph: Graph,
        students_map: dict[int, Student],
        teachers_map: dict[int, Teacher],
        courses_map: dict[int, Course],
        genes: dict[int, int] = None
    ) -> None:
        self.__graph = graph  # needed to create correct mutations and offstring
        self.__courses_map = courses_map  # needed to get the teacher id of a course
        self.__teachers_map = teachers_map # needed to get the preferences of a teacher
        self.__students_map = students_map # needed to compute penalties based on students' timetable
        self.__genes = genes
        if not genes:
            self.__genes = {}

    def get_colouring(self) -> dict:
        return self.__genes

    def get_teacher_id(self, course: int):
        return self.__courses_map[course].teacher_id

    def get_used_colours(self) -> List:
        used_colours = []
        for course_id in self.__genes:
            if self.__genes[course_id] not in used_colours:
                used_colours.append(self.__genes[course_id])
        return used_colours

    def penalty(self) -> int:
        # TODO: apply the other penalties (overcrowding, uniformity, etc)
        penalty = 0
        # Invalid colouring penalty
        for course in self.__genes:
            penalty += Constants.IVALID_COLOURING_PENALTY if not self.__graph.valid_colouring_for(
                course, self.__genes) else 0
        # Overcrowding penalty - applied if a student/teacher has more than 6 courses in a day 
        return penalty

    # Fitness function based on weights for teacher preferences and penalties for incorrect solutions
    def fitness(self) -> int:
        score = 0
        for course in self.__genes:
            teacher_id = self.__courses_map[course].teacher_id
            weights = self.__teachers_map[teacher_id].weights
            weighted_sum = 1 # sum(weights)
            score += weights[self.__genes[course]] / weighted_sum

        fitness = score * len(self.get_used_colours())
        return fitness + self.penalty()

    # One cut crossover function
    # changes entire classes of colours
    def crossover(self, other) -> Tuple:
        parent1_colours = self.get_used_colours()
        parent2_colours = other.get_used_colours()

        cut_point = randint(1, min(len(parent1_colours), len(parent2_colours)) - 1)

        offspring1_colours  = deepcopy(parent1_colours)
        offspring2_colours = deepcopy(parent2_colours)

        for i in range(cut_point, min(len(offspring1_colours), len(parent2_colours))):
            offspring1_colours[i] = parent2_colours[i]
        
        for i in range(cut_point, min(len(offspring2_colours), len(parent1_colours))):
            offspring2_colours[i] = parent1_colours[i]

        offspring1 = deepcopy(self.__genes)
        offspring2 = deepcopy(other.get_colouring())

        for new_colour in offspring1_colours:
            for course in offspring1:
                old_colour = offspring1[course] 
                if old_colour not in offspring1_colours: # old colour from parent 1
                    offspring1[course] = new_colour
        
        for new_colour in offspring2_colours:
            for course in offspring2:
                old_colour = offspring2[course]
                if old_colour not in offspring2_colours:  # old colour from parent 2
                    offspring2[course] = new_colour

        offspring1 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring1)
        offspring2 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring2)
        print(f'Offspring fitnesses: {offspring1.fitness()}, {offspring2.fitness()}')
        return offspring1, offspring2

    # Mutation function that randomly changes an entire colour class
    def mutate(self, probability: int, colour_set: List) -> None:
        p = randint(0, 100)
        if p > probability:
            return
        colours = self.get_used_colours()
        idx = randint(0, len(colours) - 1)
        old_colour = colours[idx]
        unused_colours = np.setdiff1d(np.array(colour_set), np.array(colours))
        idx = randint(0, len(unused_colours) - 1)
        new_colour = unused_colours[idx]
        for course in self.__genes:
            if self.__genes[course] == old_colour:
                self.__genes[course] = new_colour
