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


class Chromosome:
    def __init__(self, graph: Graph, genes: dict = None) -> None:
        self.__graph = graph # needed to create correct mutations and offstring
        self.__genes = genes
        if not genes:
            self.__genes = {}

    def get_colouring(self) -> dict:
        return self.__genes

    def fitness(self) -> int:
        # TODO: implement fitness function
        return 0

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
    
        return list(map(lambda result: Chromosome(graph=self._graph, genes=result), results))

    # Selection method: used to select 2 parents that will produce offspring
    # The function returns parent1 and it's index alongside parent2 and it's index
    def __selection(self, population: List[Chromosome]) -> Tuple[Chromosome, int, Chromosome, int]:
        # TODO: implemant selection method (tournament, etc)
        return (population[0], 0, population[1], 1)

    def run(self, colours_set: List) -> dict:
        population = self.__generate_population(colours_set)
        for generation in range(self.generations_cnt):
            print(f'Generation {generation}')
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
