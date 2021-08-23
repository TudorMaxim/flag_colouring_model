from enum import Enum


class EvolutionaryAlgorithmConfig(Enum):
    GENERATIONAL_POPULATION = 'generational'
    STEADY_STATE_POPULATION = 'steady_state'
    ROULETTE_WHEEL_SELECTION = 'roulette_wheel'
    TOURNAMENT_SELECTION = 'tournament'
    ONE_POINT_CROSSOVER = 'one_point'
    TWO_POINTS_CROSSOVER = 'two_points'
    UNIFORM_CROSSOVER = 'uniform'
