'''
graph.py -- William Bailey -- April 2024
A basic class implementation of a weighted, directed graph.
'''
from __future__ import annotations
from abc import abstractmethod, ABC
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_random_cities(num_cities):
    city_locations = np.random.normal(loc=0, scale=1, size=(num_cities, 2))
    return city_locations


def create_graph_from_cities(city_locations):
    num_cities = len(city_locations)
    names = [f"City{i}" for i in range(num_cities)]
    weights = np.zeros((num_cities, num_cities))

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                dist = np.linalg.norm(city_locations[i] - city_locations[j])
                weights[i][j] = dist
            else:
                weights[i][j] = 0

    return Graph(names, weights, city_locations)



class Graph:
    '''
    Represents a weighted, directed graph.
    '''
    def __init__(self, node_names: list, weights: np.ndarray, city_locations=None):
        '''
        Construct a Graph object from a list of node names,
        and the weights on the edges between them.
        '''
        assert len(weights) == len(weights[0]) and len(weights) == len(node_names), 'Size mismatch!'
        self.node_names = node_names
        self.nodes = list(range(len(self.node_names)))
        self.weights = weights
        self.city_locations = city_locations


    def weight_from_i_to_j(self, i: int, j: int) -> int:
        '''
        Returns the weight on the edge from vertex i to vertex j.
        '''
        return self.weights[i][j]


    def get_tour_weight(self, tour):
        '''
        Returns the total weight of traveling the entire circuit from
        tour[0] tour[1], ..., tour[N-1], tour[0]
        '''
        return sum(self.weights[tour[i-1]][tour[i]] for i in range(0, len(tour)))


    def get_node_locations(self) -> np.ndarray:
        return self.city_locations


    def get_city_name_for_index(self, i):
        return self.node_names[i]


    def generate_nna_tour(self) -> list:
        N = len(self.nodes)
        edges = []
        for i in range(N):
            for j in range(i+1, N):
                edges.append([i, j, self.weight_from_i_to_j(i, j)]) # Assumes undirected graph.

        edges.sort(key=lambda tpl: tpl[2]) # Sort by weight

        tour = []
        for edge in edges:
            if len(tour) == N:
                break

            v1, v2, weight = edge
            if degree_in_tour(v1, tour) < 2 and degree_in_tour(v2, tour) < 2:
                tour.append(edge)
                print(tour)

        return tour


def degree_in_tour(i: int, tour: list[tuple[int,int,float]]) -> int:
    if len(tour) == 0:
        return 0

    return sum(i in edge[:2] for edge in tour)


class TSPIndividual():
    '''
    An abstract base class which outlines common elements
    of TSPindividual solutions in a genetic algorithm.
    '''
    def __init__(self, graph: Graph, tour: list[int] = None):
        self.graph = graph
        self.tour = tour if tour else random.sample(graph.nodes, len(graph.nodes))


    def fitness(self) -> float:
        return self.graph.get_tour_weight(self.tour)


    def __lt__(self, other: TSPIndividual) -> bool:
        '''
        Implements < operator. Returns True if calling
        object is more fit than other TSPIndividual.
        '''
        return self.fitness() < other.fitness()


    def crossover_with(self, other: TSPIndividual) -> list[TSPIndividual]:
        '''
        Combines the calling object with another TSPIndividual
        in a problem-specific way to produce new TSPIndividual objects.
        '''
        remaining = set(self.tour)
        current = random.choice(self.tour)
        child = [current]
        remaining.remove(current)

        while remaining:
            index_self = self.tour.index(current)
            index_other = other.tour.index(current)

            next_self = self.tour[(index_self + 1) % len(self.tour)]
            next_other = other.tour[(index_other + 1) % len(other.tour)]

            candidates = [c for c in [next_self, next_other] if c in remaining]
            if not candidates:
                current = remaining.pop()
            else:
                current = min(candidates, key=lambda c: self.graph.weight_from_i_to_j(child[-1], c))
                remaining.remove(current)
            child.append(current)

        return [TSPIndividual(self.graph, child)]
    


    def mutate_with_probability(self, p: float) -> None:
        '''Mutates the calling object with probability p.'''
        if random.random() < p:
            i = random.randint(0, len(self.tour) - 2)
            self.tour[i], self.tour[i + 1] = self.tour[i + 1], self.tour[i]



class TSPGeneticAlgorithm():
    '''
    An abstract base class which outlines common elements of a genetic algorithm.
    '''
    def __init__(self, graph: Graph, population_size: int, mutation_prob: float):
        self.graph = graph
        self.population_size = population_size
        self.mutation_prob = mutation_prob
        self.population = [
            self.TSPcreate_new_individual()
            for _ in range(self.population_size)
        ]
        self.population.sort() # uses TSPIndividual.__lt__()        


    def TSPcreate_new_individual(self) -> TSPIndividual:
        return TSPIndividual(self.graph)


    def reproducing_subset(self) -> list[TSPIndividual]:
        return self.population[:len(self.population) // 2]


    def run_genetic_algorithm(self, max_generations: int):
        # NOTE: self.population initialized in constructor
        for _ in range(max_generations):
            reproducers = self.reproducing_subset()

            while len(reproducers) >= 2:
                parent1 = reproducers.pop(random.randint(0, len(reproducers)-1))
                parent2 = reproducers.pop(random.randint(0, len(reproducers)-1))
                children = parent1.crossover_with(parent2)
                for child in children:
                    child.mutate_with_probability(self.mutation_prob)

                self.population.extend(children)
                self.population.sort()
                self.population = self.population[:self.population_size]

        return self.population[0]


def run_tsp(num_cities, num_iterations, mutation_prob):
    cities = generate_random_cities(num_cities)
    graph = create_graph_from_cities(cities)
    ga = TSPGeneticAlgorithm(graph, population_size=100, mutation_prob=mutation_prob)

    best_fitnesses = []
    for _ in range(num_iterations):
        best = ga.run_genetic_algorithm(1)  # Run 1 generation at a time
        best_fitnesses.append(best.fitness())

    # Plot result
    plt.plot(best_fitnesses)
    plt.xlabel("Generation")
    plt.ylabel("Tour Distance")
    plt.title("TSP Genetic Algorithm")
    plt.grid(True)
    plt.show()

    return best




if __name__ == "__main__":
    num_cities = 50
    num_iterations = 100
    mutation_prob = 0.0
    best = run_tsp(num_cities, num_iterations, mutation_prob)
    print(f'Final best: {best.fitness()}')