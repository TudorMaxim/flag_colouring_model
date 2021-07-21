import numpy as np
from typing import List, Tuple
from random import randint
from model.Graph import Graph
from utils import Constants


# TODO: update and store this weights for each teacher
# 2 - preferred time slot
# 4 - indifferent
# 8 - unpreferred time slot
weights = [0] + [8, 2, 2, 2, 2, 8, 2, 2, 4, 4, 4, 8] * 5


class Chromosome:
    def __init__(self, graph: Graph, courses_map: dict, genes: dict = None) -> None:
        self.__graph = graph  # needed to create correct mutations and offstring
        self.__courses_map = courses_map  # needed to get the teacher of a course
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
        return penalty

    # Fitness function based on weights for teacher preferences and penalties for incorrect solutions
    def fitness(self) -> int:
        score = 0
        for course in self.__genes:
            # TODO: get the weights of each teacher, not the predefined ones
            score += weights[self.__genes[course]]

        fitness = score / len(self.get_used_colours()) # devided by total weights
        return fitness + self.penalty()

    # Two point crossover function
    # change entire classes of colours
    def crossover(self, other) -> Tuple:
        offspring1 = {}
        offspring2 = {}
        max_value = len(self.__genes.keys())
        middle = max_value // 2
        point1 = randint(1, middle)
        point2 = randint(middle, max_value - 1)

        for i in self.__genes.keys():
            offspring1[i] = self.__genes[i]
            offspring2[i] = other.get_colouring()[i]

        for i in range(point1 + 1, point2):
            offspring1[i] = other.get_colouring()[i]
            offspring2[i] = self.__genes[i]

        offspring1 = Chromosome(self.__graph, self.__courses_map, offspring1)
        offspring2 = Chromosome(self.__graph, self.__courses_map, offspring2)
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
