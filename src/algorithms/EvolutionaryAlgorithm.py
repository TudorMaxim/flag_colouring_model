import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
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


class EvolutionaryAlgorithm(AbstractColouringAlgorithm):
    def __init__(
        self,
        graph: Graph,
        students_map: dict[int, Student] = None,
        teachers_map: dict[int, Teacher] = None,
        courses_map: dict[int, Course] = None
    ) -> None:
        super().__init__(graph, students_map, teachers_map, courses_map)
        self.generations_cnt = Constants.GENERATIONS_CNT
        self.population_cnt = Constants.POPULATION_CNT
        self.mutation_probability = Constants.MUTATION_PROBABILITY
    
    def __heuristic_task(self, algorithm: AbstractColouringAlgorithm, colours_set: List, results: List, index: int) -> None:
        results[index] = algorithm.run(colours_set)

    # only valid solutions
    # Try: replace entire pop
    # Function that generates a population of valid solutions
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

        population = list(map(lambda result: Chromosome(
            graph=self._graph,
            students_map=self.students_map,
            teachers_map=self.teachers_map,
            courses_map=self.courses_map,
            genes=result
        ), results))

        # Mutate the population to obtain more diversity
        for i in range(3, len(population)):
            if i % 3 == 0:
                population[i].colour_class_mutation(probability=100, colour_set=colours_set)
            elif i % 3 == 1:
                population[i].colour_class_split_mutation(probability=100, colour_set=colours_set)
            else:
                extra_colours = randint(1, Constants.COLOURS_CNT)
                for _ in range(extra_colours):
                    population[i].single_colour_mutation(probability=100, colour_set=colours_set)
        
        fitnesses = list(map(lambda ch: ch.fitness(), population))
        print('Population Fitnesses:')
        print(fitnesses)
        unique = np.unique(np.array(fitnesses))
        print('\nUnique fitnesses:')
        print(unique)
        diversity = len(unique) / len(fitnesses)
        print(f'Population diversity ratio: {diversity}\n')

        return population

    def __roulette_wheel(self, population: List[Chromosome], chosen: List[bool]) -> Tuple[Chromosome, int]:
        fitness_sum = int(sum(list(map(lambda chromosome: chromosome.fitness(), population))))
        fixed_point = randint(0, fitness_sum)
        idx = 0
        partial_sum = 0
        while partial_sum < fixed_point and idx < len(population):
            partial_sum += population[idx].fitness() if not chosen[idx] else 0
            idx += 1
        if idx == len(population):
            return population[-1], len(population) - 1
        return population[idx], idx
    
    # Roulette Wheel Selection
    # The method selects 2 parents to produce offspring
    # Returns 2 chromosome objects and their indices.
    def __selection(self, population: List[Chromosome]) -> Tuple[Chromosome, int, Chromosome, int]:
        chosen = [False for _ in population]
        parent1, i = self.__roulette_wheel(population, chosen)
        chosen[i] = True
        parent2, j = self.__roulette_wheel(population, chosen)
        print(f'Selected parents: {i} and {j}')
        return parent1, i, parent2, j

    def run(self, colours_set: List) -> dict:
        # Steady State population
        population = self.__generate_population(colours_set)
        x_axis = [i for i in range(1, self.generations_cnt + 1)]
        y_axis = []
        for generation in range(self.generations_cnt):
            parent1, i, parent2, j = self.__selection(population)
            offspring1, offspring2 = parent1.crossover(parent2)
            offspring1.colour_class_mutation(self.mutation_probability, colours_set)
            offspring2.colour_class_mutation(self.mutation_probability, colours_set)
            offspring1.single_colour_mutation(self.mutation_probability, colours_set)
            offspring2.single_colour_mutation(self.mutation_probability, colours_set)

            # Keep only the best 2 solutions in the population
            options = sorted(
                [offspring1, offspring2, population[i], population[j]],
                key=lambda chromosome: chromosome.fitness()
            )
            population[i] = options[0]
            population[j] = options[1]

            best = min(population, key=lambda chromosome: chromosome.fitness())
            y_axis.append(best.fitness())
            
            print(f'Generation {generation}')
            print(f'Best fitness: {best.fitness()}\n')
        
        plt.plot(x_axis, y_axis)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title('Evolution of the best individual within the population')
        plt.show()

        best = min(population, key=lambda chromosome: chromosome.fitness())
        return best.get_colouring()
