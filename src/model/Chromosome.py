from copy import deepcopy
import numpy as np
from typing import List, Tuple
from random import choice, randint
from model.Course import Course
from model.Graph import Graph
from model.Person import Person
from model.Student import Student
from model.Teacher import Teacher
from utils import Constants
from utils.Helpers import Helpers
from algorithms.EvolutionaryAlgorithmConfig import EvolutionaryAlgorithmConfig


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

    def copy(self):
        return Chromosome(
            graph=self.__graph,
            students_map=self.__students_map,
            teachers_map=self.__teachers_map,
            courses_map=self.__courses_map,
            genes=deepcopy(self.__genes)
        )
    
    def get_colouring(self) -> dict:
        return self.__genes

    def get_teacher_id(self, course: int):
        return self.__courses_map[course].teacher_id

    # Function that computes the overcrowding penalty.
    # e.g.: a person has more than 6 courses a day.
    def __overcrowding(self, person: Person) -> int:
        penalty = 0
        frequency = [0] * 5
        for course in person.course_ids:
            colour = self.__genes[course]
            day = (colour - 1) // 12
            frequency[day] += 1
        for f in frequency:
                penalty += Constants.OVERCROWDING_PENALTY if f > Constants.MAX_COURSES_PER_DAY else 0
        return penalty

    # Function that computes the fragmentation penalty
    # e.g.: A teacher that has a break longer than 2 hours
    def __fragmentation(self, teacher: Teacher) -> int:
        penalty = 0
        timetable = []
        for course in teacher.course_ids:
            colour = self.__genes[course]
            day = (colour - 1) // 12
            timetable.append((colour, day))
        timetable = sorted(timetable)
        for i in range(1, len(timetable)):
            if timetable[i][1] == timetable[i - 1][1] and \
                abs(timetable[i][0] - timetable[i - 1][0]) > Constants.MAX_DAILY_BREAK:
                penalty += Constants.FRAGMENTATION_PENALTY
        return penalty
    
    # Function that computes the uniformity penalty
    # This penalty represents the difference between the longest and shortest day of a person.
    def __uniformity(self, person: Person) -> int:
        classes = [0] * 5
        for course in person.course_ids:
            colour = self.__genes[course]
            day = (colour - 1) // 12
            classes[day] += 1
        shortest_day = min(classes)
        longest_day = max(classes)
        return (longest_day - shortest_day) * Constants.UNIFORMITY_PENALTY
    
    # Function that computes the overall penalty of a chromosome
    def penalty(self) -> int:
        penalty = 0
        for course in self.__genes:
            penalty += Constants.IVALID_COLOURING_PENALTY if not self.__graph.valid_colouring_for(course, self.__genes) else 0
        
        for student_id in self.__students_map:
            penalty += self.__overcrowding(self.__students_map[student_id])
            penalty += self.__uniformity(self.__students_map[student_id])

        for teacher_id in self.__teachers_map:
            penalty += self.__overcrowding(self.__teachers_map[teacher_id])
            penalty += self.__fragmentation(self.__teachers_map[teacher_id])
            penalty += self.__uniformity(self.__teachers_map[teacher_id])

        return penalty

    # Fitness function based on weights for teacher preferences and various penalties
    def fitness(self) -> float:
        numerator = 0
        denominator = 0
        for course in self.__genes:
            teacher_id = self.__courses_map[course].teacher_id
            weights = self.__teachers_map[teacher_id].weights
            weight = weights[self.__genes[course]]
            day = ((self.__genes[course] - 1) // 12) + 1
            hour = ((self.__genes[course] - 1) % 12) + 1
            numerator += weight * day * hour
            denominator += weight

        score = numerator / denominator
        fitness = score * Helpers.get_used_colours_count(self.__genes)
        return fitness + self.penalty()

    def __one_point_crossover(self, other) -> Tuple:
        parent1 = list(map(lambda item: item[1], sorted(self.__genes.items(), key=lambda item: item[0])))
        parent2 = list(map(lambda item: item[1], sorted(other.get_colouring().items(), key=lambda item: item[0])))
        assert(len(parent1) == len(parent2))
        
        courses_cnt = len(parent1)
        cut_point = randint(1, courses_cnt - 1)
        offspring1_colours = [0] * courses_cnt
        offspring1_colours[:cut_point] = parent1[:cut_point]
        offspring1_colours[cut_point:] = parent2[cut_point:]
        offspring2_colours = [0] * courses_cnt
        offspring2_colours[:cut_point] = parent2[:cut_point]
        offspring2_colours[cut_point:] = parent1[cut_point:]

        offspring1 = {}
        offspring2 = {}
        for i in range(len(offspring1_colours)):
            offspring1[i + 1] = offspring1_colours[i]
        for i in range(len(offspring2_colours)):
            offspring2[i + 1] = offspring2_colours[i]
        
        offspring1 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring1)
        offspring2 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring2)
        return offspring1, offspring2

    def __two_points_crossover(self, other) -> Tuple:
        parent1 = list(map(lambda item: item[1], sorted(self.__genes.items(), key=lambda item: item[0])))
        parent2 = list(map(lambda item: item[1], sorted(other.get_colouring().items(), key=lambda item: item[0])))
        assert(len(parent1) == len(parent2))

        courses_cnt = len(parent1)
        cut_point1 = randint(1, courses_cnt / 2)
        cut_point2 = randint(cut_point1 + 1, courses_cnt - 1)
        offspring1_colours = [0] * courses_cnt
        offspring1_colours[:cut_point1] = parent1[:cut_point1]
        offspring1_colours[cut_point1:cut_point2] = parent2[cut_point1:cut_point2]
        offspring1_colours[cut_point2:] = parent1[cut_point2:]
        offspring2_colours = [0] * courses_cnt
        offspring2_colours[:cut_point1] = parent2[:cut_point1]
        offspring2_colours[cut_point1:cut_point2] = parent1[cut_point1:cut_point2]
        offspring2_colours[cut_point2:] = parent2[cut_point2:]

        offspring1 = {}
        offspring2 = {}
        for i in range(len(offspring1_colours)):
            offspring1[i + 1] = offspring1_colours[i]
        for i in range(len(offspring2_colours)):
            offspring2[i + 1] = offspring2_colours[i]

        offspring1 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring1)
        offspring2 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring2)
        return offspring1, offspring2

    def __uniform_crossover(self, other) -> Tuple:
        parent1 = list(map(lambda item: item[1], sorted(self.__genes.items(), key=lambda item: item[0])))
        parent2 = list(map(lambda item: item[1], sorted(other.get_colouring().items(), key=lambda item: item[0])))
        assert(len(parent1) == len(parent2))

        selection = [randint(0, 1) for _ in range(len(parent1))]
        offspring1 = {}
        offspring2 = {}
        for i in range(len(selection)):
            if selection[i] == 0:
                offspring1[i + 1] = parent1[i]
                offspring2[i + 1] = parent2[i]
            else:
                offspring2[i + 1] = parent1[i]
                offspring1[i + 1] = parent2[i]
        offspring1 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring1)
        offspring2 = Chromosome(self.__graph, self.__students_map, self.__teachers_map, self.__courses_map, offspring2)
        return offspring1, offspring2
    
    def crossover(self, other, method: EvolutionaryAlgorithmConfig = EvolutionaryAlgorithmConfig.ONE_POINT_CROSSOVER) -> Tuple:
        if method == EvolutionaryAlgorithmConfig.ONE_POINT_CROSSOVER:
            return self.__one_point_crossover(other)
        elif method == EvolutionaryAlgorithmConfig.TWO_POINTS_CROSSOVER:
            return self.__two_points_crossover(other)
        else:
            return self.__uniform_crossover(other)
    
    # Mutation function that randomly changes an entire colour class
    def colour_class_mutation(self, probability: int, colour_set: List[int]) -> None:
        p = randint(0, 100)
        if p > probability:
            return
        colours = Helpers.get_used_colours(self.__genes)
        idx = randint(0, len(colours) - 1)
        old_colour = colours[idx]
        unused_colours = np.setdiff1d(np.array(colour_set), np.array(colours))
        if not len(unused_colours):
            return 
        idx = randint(0, len(unused_colours) - 1)
        new_colour = unused_colours[idx]
        for course in self.__genes:
            if self.__genes[course] == old_colour:
                self.__genes[course] = new_colour

    # Mutation function that randomly changes the colour of a course
    def single_colour_mutation(self, probability: int, colour_set: List[int]) -> None:
        p = randint(0, 100)
        if p > probability:
            return
        colours = Helpers.get_used_colours(self.__genes)
        course_id = randint(1, len(self.__courses_map.values()) - 1)
        unused_colours = np.setdiff1d(np.array(colour_set), np.array(colours))
        if not len(unused_colours):
            return
        new_colour = choice(unused_colours)
        self.__genes[course_id] = new_colour

    # Mutation function that selects an used colour and keeps only half of the nodes coloured as before.
    # The other half is re-coloured using an unused colour 
    def colour_class_split_mutation(self, probability: int, colour_set: List[int]) -> None:
        p = randint(0, 100)
        if p > probability:
            return
        colours = Helpers.get_used_colours(self.__genes)
        idx = randint(0, len(colours) - 1)
        old_colour = colours[idx]
        unused_colours = np.setdiff1d(np.array(colour_set), np.array(colours))
        if not len(unused_colours):
            return
        idx = randint(0, len(unused_colours) - 1)
        new_colour = unused_colours[idx]
        cnt = 0
        for course in self.__genes:
            if self.__genes[course] == old_colour and cnt % 2 == 0:
                self.__genes[course] = new_colour
            cnt += 1

    def mutate(self, probability: int, colour_set: List[int]) -> None:
        colour_class_mutant = self.copy()
        colour_class_mutant.colour_class_mutation(probability, colour_set)
        single_colour_mutant = self.copy()
        single_colour_mutant.single_colour_mutation(probability, colour_set)
        colour_class_split_mutant = self.copy()
        colour_class_split_mutant.colour_class_split_mutation(probability, colour_set)
        self = min([
            self,
            colour_class_mutant,
            colour_class_split_mutant,
            single_colour_mutant
        ], key=lambda chromosome: chromosome.fitness())
