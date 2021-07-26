import matplotlib.pyplot as plt
import numpy as np
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


class EvolutionaryAlgorithmConfig(Enum):
    GENERATIONAL_POPULATION = 'generational'
    STEADY_STATE_POPULATION = 'steady_state'
    ROULETTE_WHEEL_SLECTION = 'roulette_wheel'
    TOURNAMENT_SELECTION = 'tournament'

class EvolutionaryAlgorithm(AbstractColouringAlgorithm):
    def __init__(
        self,
        graph: Graph,
        students_map: dict[int, Student] = None,
        teachers_map: dict[int, Teacher] = None,
        courses_map: dict[int, Course] = None,
        population_model: str = EvolutionaryAlgorithmConfig.GENERATIONAL_POPULATION,
        selection_method: str = EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SLECTION
    ) -> None:
        super().__init__(graph, students_map, teachers_map, courses_map)
        self.generations_cnt = Constants.GENERATIONS_CNT
        self.population_cnt = Constants.POPULATION_CNT
        self.mutation_probability = Constants.MUTATION_PROBABILITY
        self.population_model = population_model
        self.selection_method = selection_method
    
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
        unique = np.unique(np.array(fitnesses))
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
    
    # Tournament selection
    # Select the best chromosome out of k random ones.
    def __tournament(self, population: List[Chromosome], k: int = 2) -> Tuple[Chromosome, int]:
        if k < 2:
            raise ValueError('Error: you must select at least 2 solutions to compete in tournament selection')
        choices = shuffle(range(len(population)))
        choices = choices[0 : k]
        best = None
        pos = -1
        for i in range(k):
            if best is None or population[choices[i]].fitness() < best.fitness():
                best  = population[choices[i]]
                pos = i
        return best, pos


    # Roulette Wheel Selection
    # The method selects 2 parents to produce offspring
    # Returns 2 chromosome objects and their indices.
    def __selection(self, population: List[Chromosome]) -> Tuple[Chromosome, int, Chromosome, int]:
        if self.selection_method == EvolutionaryAlgorithmConfig.ROULETTE_WHEEL_SLECTION:
            chosen = [False for _ in population]
            parent1, i = self.__roulette_wheel(population, chosen)
            chosen[i] = True
            parent2, j = self.__roulette_wheel(population, chosen)
        else:
            parent1, i = self.__tournament(population)
            parent2, j = self.__tournament(population)
        
        print(f'Selected parents: {i} and {j}')
        return parent1, i, parent2, j

    def __get_best(self, population: List[Chromosome]) -> Chromosome:
       return min(population, key=lambda chromosome: chromosome.fitness())

    def __steady_state(self, colours_set: List[int]) -> dict[int, int]:
        # Steady State population
        population = self.__generate_population(colours_set)
        best = self.__get_best(population)
        x_axis = [i for i in range(0, self.generations_cnt + 1)]
        y_axis = [best.fitness()]
        for generation in range(self.generations_cnt):
            parent1, i, parent2, j = self.__selection(population)
            offspring1, offspring2 = parent1.crossover(parent2)
            offspring1.colour_class_mutation(self.mutation_probability, colours_set)
            offspring2.colour_class_mutation(self.mutation_probability, colours_set)
            offspring1.single_colour_mutation(self.mutation_probability, colours_set)
            offspring2.single_colour_mutation(self.mutation_probability, colours_set)
            offspring1.colour_class_split_mutation(self.mutation_probability, colours_set)
            offspring2.colour_class_split_mutation(self.mutation_probability, colours_set)

            # Keep only the best 2 solutions in the population
            options = sorted(
                [offspring1, offspring2, population[i], population[j]],
                key=lambda chromosome: chromosome.fitness()
            )
            population[i] = options[0]
            population[j] = options[1]

            best = self.__get_best(population)
            y_axis.append(best.fitness())
            
            print(f'Generation {generation}')
            print(f'Best fitness: {best.fitness()}\n')
        
        plt.plot(x_axis, y_axis)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title('Evolution of the best individual within the population')
        plt.show()
        return best.get_colouring()

    # Generational population
    # At each generation, the entire population is replaced with the offspring   
    def __generational(self, colours_set: List[int]) -> dict[int, int]:
        population = self.__generate_population(colours_set)
        best = self.__get_best(population)
        x_axis = [i for i in range(0, self.generations_cnt + 1)]
        y_axis = [best.fitness()]
        for generation in range(self.generations_cnt):
            # 2-Tournament selection - shuffle the population and select pairs of consecutive chromosomes.
            shuffle(population)
            next_generation = []
            for i in range(1, len(population), 2):
                offspring1, offspring2 = population[i].crossover(population[i - 1])
                offspring1.colour_class_mutation(self.mutation_probability, colours_set)
                offspring2.colour_class_mutation(self.mutation_probability, colours_set)
                offspring1.single_colour_mutation(self.mutation_probability, colours_set)
                offspring2.single_colour_mutation(self.mutation_probability, colours_set)
                offspring1.colour_class_split_mutation(self.mutation_probability, colours_set)
                offspring2.colour_class_split_mutation(self.mutation_probability, colours_set)
                next_generation.append(offspring1)
                next_generation.append(offspring2)
            
            population = next_generation
            current = self.__get_best(population)
            if current.fitness() < best.fitness():
                best = current
            y_axis.append(best.fitness())
            print(f'Generation {generation}')
            print(f'Best fitness: {best.fitness()}\n')
        
        plt.plot(x_axis, y_axis)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title('Evolution of the best individual within the population')
        plt.show()
        return best.get_colouring()


    def run(self, colours_set: List) -> dict:
        print(f'Using a {self.population_model} population with {self.population_cnt} individuals.')
        print(f'Using {self.selection_method} selection.\n')
        if self.population_model == EvolutionaryAlgorithmConfig.STEADY_STATE_POPULATION:
            return self.__steady_state(colours_set)
        return self.__generational(colours_set)
