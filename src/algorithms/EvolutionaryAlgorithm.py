from typing import List, Tuple
from time import sleep
from random import randint, shuffle
from threading import Thread
from model.Graph import Graph
from utils import Constants
from algorithms.AbstractColouringAlgorithm import AbstractColouringAlgorithm
from algorithms.LargestDegreeOrdering import LargestDegreeOrdering
from algorithms.DegreeOfSaturation import DegreeOfSaturation
from algorithms.RecursiveLargestFirst import RecursiveLargestFirst

# TODO: update and store this weights for each teacher
# 2 - preferred time slot
# 4 - indifferent
# 8 - unpreferred time slot  
weights = [0] + [8, 2, 2, 2, 2, 8, 2, 2, 4, 4, 4, 8] * 5

class Chromosome:
    def __init__(self, graph: Graph, courses_map: dict, genes: dict = None) -> None:
        self.__graph = graph # needed to create correct mutations and offstring
        self.__courses_map = courses_map # needed to get the teacher of a course
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

    # Fitness function based on weights for teacher preferences and penalties for incorrect solutions

    def penalty(self) -> int:
        # TODO: apply the other penalties (overcrowding, uniformity, etc)
        penalty = 0
        # Invalid colouring penalty
        for course in self.__genes:
            penalty += Constants.IVALID_COLOURING_PENALTY if not self.__graph.valid_colouring_for(course, self.__genes) else 0
        return penalty

    def fitness(self) -> int:
        score = 0
        for course in self.__genes:
            # TODO: get the weights of each teacher, not the predefined ones
            score += weights[self.__genes[course]]

        fitness = score / len(self.get_used_colours())
        return fitness + self.penalty()

    def crossover(self, other):
        # TODO: implement crossover function
        return self, other

    def mutate(self, probability: int) -> None:
        p = randint(0, 100)
        if p <= probability:
            # TODO: mutate the chromosome
            pass


class EvolutionaryAlgorithm(AbstractColouringAlgorithm):
    def __init__(self, graph: Graph, courses_map: dict) -> None:
        super().__init__(graph, courses_map)
        self.generations_cnt = Constants.GENERATIONS_CNT
        self.population_cnt = Constants.POPULATION_CNT
        self.mutation_probability = Constants.MUTATION_PROBABILITY
    
    def __heuristic_task(self, algorithm: AbstractColouringAlgorithm, colours_set: List, results: List, index: int) -> None:
        results[index] = algorithm.run(colours_set)

    def __generate_population(self, colours_set: List) -> List[Chromosome]:
        heuristics = [
            LargestDegreeOrdering(self._graph),
            DegreeOfSaturation(self._graph),
            RecursiveLargestFirst(self._graph)
        ]
        colours_sets = [None] * 3
        threads = [None] * 3
        positions = [{}] * 3
        results = [{}] * self.population_cnt

        for i in range(3):
            colours_sets[i] = colours_set
            shuffle(colours_set)

        for i in range(3):
            for j in range(len(colours_set)):
                positions[i][colours_sets[i][j]] = j
            threads[i] = Thread(target=self.__heuristic_task, args=(heuristics[i], colours_sets[i], results, i,))
            threads[i].start()

        for i in range(3):
            threads[i].join()
        
        for i in range(3, self.population_cnt): 
            shuffle(colours_set)
            for vertex in self._graph.get_vertices():
                idx = randint(0, 2)
                old_colour = results[idx][vertex]
                position = positions[idx][old_colour]
                results[i][vertex] = colours_set[position]
    
        for colouring in results:
            assert self._graph.valid_colouring(colour_map=colouring)
    
        return list(map(lambda result: Chromosome(graph=self._graph, courses_map=self.courses_map, genes=result), results))

    def __roulette_wheel(self, population: List[Chromosome], chosen: List[bool]) -> Tuple[Chromosome, int]:
        fitness_sum = int(sum(list(map(lambda chromosome: chromosome.fitness(), population))))
        fixed_point = randint(0, fitness_sum)
        idx = -1
        partial_sum = 0
        while partial_sum < fixed_point and idx < len(population):
            idx += 1
            partial_sum += population[idx].fitness() if not chosen[idx] else 0
        return population[idx], idx
    
    # Roulette Wheel Selection
    # The method selects 2 parents to produce offspring
    # Returns 2 chromosome objects and their indices.
    def __selection(self, population: List[Chromosome]) -> Tuple[Chromosome, int, Chromosome, int]:
        chosen = [False for _ in population]
        parent1, i = self.__roulette_wheel(population, chosen)
        chosen[i] = True
        parent2, j = self.__roulette_wheel(population, chosen)
        return parent1, i, parent2, j

    def run(self, colours_set: List) -> dict:
        population = self.__generate_population(colours_set)
       
        for generation in range(self.generations_cnt):
            print(f'Generation {generation}')

            population = sorted(population, key=lambda chromosome: chromosome.fitness())
            print(f'Best fitness: {population[0].fitness()}\n')

            parent1, i, parent2, j = self.__selection(population)
            offspring1, offspring2 = parent1.crossover(parent2)
            offspring1.mutate(self.mutation_probability)
            offspring2.mutate(self.mutation_probability)

            # TODO: consider other ways of replacing parents with offsptring
            if offspring1.fitness() < parent1.fitness():
                population[i] = offspring1
            if offspring2.fitness() < parent2.fitness():
                population[j] = offspring2
            sleep(0.5)
            population = sorted(population, key=lambda chromosome: chromosome.fitness())
        return population[0].get_colouring()
