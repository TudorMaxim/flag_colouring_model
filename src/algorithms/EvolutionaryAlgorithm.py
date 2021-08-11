import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from typing import List, Tuple
from enum import Enum
from random import randint, shuffle
from threading import Thread
from model.Course import Course
from model.Graph import Graph
from model.Chromosome import Chromosome
from model.Student import Student
from model.Teacher import Teacher
from utils import Constants
from algorithms.AbstractColouringAlgorithm import AbstractColouringAlgorithm
from algorithms.LargestDegreeOrdering import LargestDegreeOrdering
from algorithms.DegreeOfSaturation import DegreeOfSaturation
from algorithms.RecursiveLargestFirst import RecursiveLargestFirst
from utils.Helpers import Helpers


class EvolutionaryAlgorithmConfig(Enum):
    GENERATIONAL_POPULATION = 'generational'
    STEADY_STATE_POPULATION = 'steady_state'
    ROULETTE_WHEEL_SELECTION = 'roulette_wheel'
    TOURNAMENT_SELECTION = 'tournament'

class EvolutionaryAlgorithm(AbstractColouringAlgorithm):
    def __init__(
        self,
        graph: Graph,
        students_map: dict[int, Student] = None,
        teachers_map: dict[int, Teacher] = None,
        courses_map: dict[int, Course] = None,
        population_model: EvolutionaryAlgorithmConfig = EvolutionaryAlgorithmConfig.GENERATIONAL_POPULATION,
        selection_method: EvolutionaryAlgorithmConfig = EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SELECTION,
    ) -> None:
        super().__init__(graph, students_map, teachers_map, courses_map)
        self.generations_cnt = Constants.GENERATIONS_CNT
        self.population_cnt = Constants.POPULATION_CNT
        self.mutation_probability = Constants.MUTATION_PROBABILITY
        self.population_model = population_model
        self.selection_method = selection_method
        self.debug = False # used to plot the evolution of the population.
    
    def __heuristic_task(self, algorithm: AbstractColouringAlgorithm, colours_set: List, results: List, index: int) -> None:
        results[index] = algorithm.run(colours_set)

    def __get_population_diverstity_ratio(self, population: List[Chromosome]) -> float:
        fitnesses = list(map(lambda ch: ch.fitness(), population))
        unique = np.unique(np.array(fitnesses))
        return len(unique) / len(fitnesses)

    def __get_average_fitness(self, population: List[Tuple[Chromosome, float]]) -> float:
        return sum(list(map(lambda pair: pair[1], population))) / len(population)
    
    def __get_best(self, population: List[Tuple[Chromosome, float]]) -> Tuple[Chromosome, float]:
       return min(population, key=lambda pair: pair[1])

    # Function that generates a population of valid solutions
    def __generate_population(self, colours_set: List[int]) -> List[Tuple[Chromosome, float]]:
        heuristics = [
            DegreeOfSaturation(self._graph),
            RecursiveLargestFirst(self._graph),
            LargestDegreeOrdering(self._graph)
        ]
        threads = [None] * 3
        results = [{}] * 3
        colours_sets = [None] * self.population_cnt
        
        for i in range(self.population_cnt):
            colours_sets[i] = deepcopy(colours_set)
            if i > 2: 
                shuffle(colours_set)

        for i in range(3):
            threads[i] = Thread(target=self.__heuristic_task, args=(heuristics[i], colours_sets[i], results, i,))
            threads[i].start()
        
        positions = Helpers.build_positions_map(colours_sets) 
        for i in range(3):
            threads[i].join()
        
        # Permutate colours
        for i in range(3, self.population_cnt):
            idx = randint(0, 2)
            result = {}
            for vertex in self._graph.get_vertices():
                old_colour = results[idx][vertex]
                position = positions[idx][old_colour]
                result[vertex] = colours_sets[i][position]
            results.append(result)

        population = list(map(lambda result: Chromosome(
            graph=self._graph,
            students_map=self.students_map,
            teachers_map=self.teachers_map,
            courses_map=self.courses_map,
            genes=result
        ), results))

        # Mutate the intial population to obtain more diversity
        for i in range(3, len(population)):
            if i % 3 == 0:
                population[i].colour_class_mutation(probability=100, colour_set=colours_set)
            elif i % 3 == 1:
                population[i].colour_class_split_mutation(probability=100, colour_set=colours_set)
            else:
                extra_colours = randint(1, Constants.COLOURS_CNT)
                for _ in range(extra_colours):
                    population[i].single_colour_mutation(probability=100, colour_set=colours_set)
        
        diversity = self.__get_population_diverstity_ratio(population)
        if self.debug:
            print(f'Population diversity ratio: {diversity}\n')
        return list(map(lambda chromosome: (chromosome, chromosome.fitness()), population))

    # Roulette Wheel selection
    # Each individual has a chance to be selected
    # The better the fitness, the higher the chance to be selected
    def __roulette_wheel(self, population: List[Tuple[Chromosome, float]], chosen: List[bool]) -> Tuple[Chromosome, int]:
        fitness_sum = int(sum(list(map(lambda pair: pair[1], population))))
        fixed_point = randint(0, fitness_sum)
        idx = 0
        partial_sum = 0
        while partial_sum < fixed_point and idx < len(population):
            partial_sum += population[idx][1] if not chosen[idx] else 0
            idx += 1
        if idx == len(population):
            return population[-1][0], len(population) - 1
        return population[idx][0], idx
    
    # Tournament selection
    # Select the best chromosome out of k random ones.
    def __tournament(self, population: List[Tuple[Chromosome, float]], k: int = 2) -> Tuple[Chromosome, int]:
        if k < 2:
            raise ValueError('Error: you must select at least 2 solutions to compete in tournament selection')
        choices = [i for i in range(len(population))]
        shuffle(choices)
        best = None
        best_fitness = None
        pos = -1
        for i in range(k):
            if best is None or population[choices[i]][1] < best_fitness:
                best = population[choices[i]][0]
                best_fitness = population[choices[i]][1]
                pos = choices[i]
        return best, pos

    # The method selects 2 parents using eather roulette wheel or tournament approach.
    # Returns 2 Chromosome objects and their indices.
    def __selection(self, population: List[Tuple[Chromosome, float]]) -> Tuple[Chromosome, int, Chromosome, int]:
        if self.selection_method == EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SELECTION:
            chosen = [False for _ in population]
            parent1, i = self.__roulette_wheel(population, chosen)
            chosen[i] = True
            parent2, j = self.__roulette_wheel(population, chosen)
        else:
            parent1, i = self.__tournament(population)
            parent2, j = self.__tournament(population)
        return parent1, i, parent2, j

    # Steady State EA - 2 parents are selected to produce offspring
    # The offspring replace the parents if their fitness is better. 
    def __steady_state(self, colours_set: List[int]) -> dict[int, int]:
        population = self.__generate_population(colours_set)
        best, fitness = self.__get_best(population)
        x_axis = [i for i in range(0, self.generations_cnt + 1)]
        best_fitness_y_axis = [fitness]
        avegare_fitness_y_axis = [self.__get_average_fitness(population)]
        for generation in range(self.generations_cnt):
            parent1, i, parent2, j = self.__selection(population)
            offspring1, offspring2 = parent1.crossover(parent2)
            offspring1.mutate(self.mutation_probability, colours_set)
            offspring2.mutate(self.mutation_probability, colours_set)

            # Keep only the best 2 solutions in the population
            options = sorted([
                (offspring1, offspring1.fitness()),
                (offspring2, offspring2.fitness()),
                population[i],
                population[j]
            ], key=lambda pair: pair[1])
            population[i] = options[0]
            population[j] = options[1]

            best, fitness = self.__get_best(population)
            best_fitness_y_axis.append(fitness)
            avegare_fitness_y_axis.append(self.__get_average_fitness(population))

            if self.debug:
                print(f'Generation {generation}')
                print(f'Best fitness: {fitness}\n')
        
        if self.debug:
            plt.plot(x_axis, best_fitness_y_axis)
            plt.plot(x_axis, avegare_fitness_y_axis)
            plt.legend(['Best Fitness', 'Average Fitness'], loc='upper right')
            plt.xlabel('Generation')
            plt.ylabel('Fitness')
            plt.title('Evolution of the population and its best individual')
            plt.show()
        return best.get_colouring()

    # Generational population
    # At each generation, the entire population is replaced with the offspring   
    def __generational(self, colours_set: List[int]) -> dict[int, int]:
        population = self.__generate_population(colours_set)
        best, fitness = self.__get_best(population)
        x_axis = [i for i in range(0, self.generations_cnt + 1)]
        best_fitness_y_axis = [fitness]
        avegare_fitness_y_axis = [self.__get_average_fitness(population)]
        for generation in range(self.generations_cnt):
            # 2-Tournament selection - shuffle the population and select pairs of consecutive chromosomes.
            shuffle(population)
            next_generation = []
            for i in range(1, len(population), 2):
                offspring1, offspring2 = population[i][0].crossover(population[i - 1][0])
                offspring1.mutate(self.mutation_probability, colours_set)
                offspring2.mutate(self.mutation_probability, colours_set)
                next_generation.append((offspring1, offspring1.fitness()))
                next_generation.append((offspring2, offspring2.fitness()))
            
            population = next_generation
            current, current_fitness = self.__get_best(population)
            if current_fitness < fitness:
                best = current
                fitness = current_fitness
            best_fitness_y_axis.append(fitness)
            avegare_fitness_y_axis.append(self.__get_average_fitness(population))
            if self.debug:
                print(f'Generation {generation}')
                print(f'Best fitness: {fitness}\n')
        
        if self.debug:
            plt.plot(x_axis, best_fitness_y_axis)
            plt.plot(x_axis, avegare_fitness_y_axis)
            plt.legend(['Best Fitness', 'Average Fitness'], loc='upper right')
            plt.xlabel('Generation')
            plt.ylabel('Fitness')
            plt.title('Evolution of the population and its best individual')
            plt.show()
        
        return best.get_colouring()

    def run(self, colours_set: List) -> dict:
        if self.debug:
            print(f'Using a {self.population_model.value} population with {self.population_cnt} individuals.')
            print(f'Using {self.selection_method.value} selection.\n')
        if self.population_model == EvolutionaryAlgorithmConfig.STEADY_STATE_POPULATION:
            return self.__steady_state(colours_set)
        elif self.population_model == EvolutionaryAlgorithmConfig.GENERATIONAL_POPULATION:
            return self.__generational(colours_set)
        else:
            raise ValueError('Invalid population model')
