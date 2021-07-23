import numpy as np
from typing import List, Tuple
from copy import deepcopy
from random import choice, randint
from model.Course import Course
from model.Graph import Graph
from model.Person import Person
from model.Student import Student
from model.Teacher import Teacher
from utils import Constants
from utils.Helpers import Helpers


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

    # Function that computes the overcrowding penalty.
    # e.g.: a person has more than 6 courses a day.
    def __overcrowding(self, person: Person) -> int:
        penalty = 0
        frequency = [0] * 5
        for course in person.course_ids:
            colour = self.__genes[course]
            day = (colour - 1) % 5
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
            day = (colour - 1) % 5
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
            day = (colour - 1) % 5
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
    def fitness(self) -> int:
        score = 0
        for course in self.__genes:
            teacher_id = self.__courses_map[course].teacher_id
            weights = self.__teachers_map[teacher_id].weights
            weighted_sum = 1 # sum(weights)
            score += weights[self.__genes[course]] / weighted_sum

        fitness = score * Helpers.get_used_colours_count(self.__genes)
        return fitness + self.penalty()

    # One cut crossover function which changes entire classes of colours
    def crossover(self, other) -> Tuple:
        parent1_colours = Helpers.get_used_colours(self.__genes)
        parent2_colours = Helpers.get_used_colours(other.get_colouring())

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
    def colour_class_mutation(self, probability: int, colour_set: List[int]) -> None:
        p = randint(0, 100)
        if p > probability:
            return
        colours = Helpers.get_used_colours(self.__genes)
        idx = randint(0, len(colours) - 1)
        old_colour = colours[idx]
        unused_colours = np.setdiff1d(np.array(colour_set), np.array(colours))
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
        idx = randint(0, len(unused_colours) - 1)
        new_colour = unused_colours[idx]
        cnt = 0
        for course in self.__genes:
            if self.__genes[course] == old_colour and cnt % 2 == 0:
                self.__genes[course] = new_colour
            cnt += 1
