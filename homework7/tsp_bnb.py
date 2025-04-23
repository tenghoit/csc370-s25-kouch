# “branch_and_bound_framework.py”
from __future__ import annotations
from bisect import insort
from copy import copy
import csv
import sys



class Node:
    def __init__(self, distance_matrix, tour=None):
        self.distance_matrix = distance_matrix
        self.tour = tour
        if self.tour is None:
            self.tour = [0]

        if len(self.tour) == len(self.distance_matrix) - 1:
            remaining_city = [city for city in range(len(self.distance_matrix)) if city not in self.tour]
            self.tour.append(remaining_city[0])
            

    
    def get_children(self) -> list[Node]:
        output = []

        for city in range(len(self.distance_matrix)):
            if city in self.tour: continue
            output.append(Node(self.distance_matrix, self.tour + [city]))

        return output 
    

    def get_value(self):

        if len(self.tour) != len(self.distance_matrix): return float('inf') # not complete

        total_cost = 0
        for i in range(len(self.tour) - 1):
            current_city = self.tour[i]
            next_city = self.tour[i + 1]
            total_cost += self.distance_matrix[current_city][next_city]
        total_cost += self.distance_matrix[self.tour[-1]][self.tour[0]] # return to origin cost

        return total_cost
    

    def get_bound(self) -> int:
        current_cost = 0

        for i in range(len(self.tour) - 1):
            current_city = self.tour[i]
            next_city = self.tour[i + 1]
            current_cost += self.distance_matrix[current_city][next_city]

        lower_bound = 0
        remaining_cities = [city for city in range(len(self.distance_matrix)) if city not in self.tour]
        # print(f'    remaining cites: {remaining_cities}')

        for city in remaining_cities:
            path_cost = float('inf')

            for destination in range(len(self.distance_matrix[city])):
                if destination == city or destination in self.tour: continue

                cost = self.distance_matrix[city][destination]
                if cost < path_cost: path_cost = cost

            if path_cost == float('inf'):
                return float('inf') # remaining city has no path left = prune
            else:
                lower_bound += path_cost


        return current_cost + lower_bound

    
    def has_better_value(self, other: Node) -> bool:
        if len(self.tour) != len(self.distance_matrix):
            return False  # Not a complete tour, can't be better

        if len(other.tour) != len(other.distance_matrix):
            return True  # Complete tour always beats incomplete

        return self.get_value() < other.get_value()


    def might_be_better_than(self, other: Node) -> bool:
        return self.get_bound() <= other.get_bound()

    
    def __lt__(self, other: Node) -> bool:
        return self.might_be_better_than(other)

    
    def __str__(self) -> str:
        return f'Tour: {self.tour} | Cost: {self.get_value()} | Bound: {self.get_bound()}'


class BranchAndBoundSolver:
    def __init__(self, tsp_file_path):
        self.distance_matrix = []
        self.cities = []

        self.read_tsp_csv(tsp_file_path)


    def __str__(self):
        output = ''

        headers = "city name"
        for city in self.cities:
            headers += f',{city}'
        headers += '\n'
        output += headers

        for city in range(len(self.distance_matrix)):
            line = f'{self.cities[city]}'
            for destination in range(len(self.distance_matrix[city])):
                line += f',{self.distance_matrix[city][destination]}'
            output += line + '\n'

        return output


    def read_tsp_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        self.cities = rows[0][1:]  # reading city names
        self.distance_matrix = []

        for row in rows[1:]:
            distances = list(map(int, row[1:]))  # skip name column
            self.distance_matrix.append(distances)
        

    def get_root(self) -> Node:
        return Node(self.distance_matrix)

    def find_solution(self):
        Q = [self.get_root()]
        best_node = Q[0]

        while Q:
            # print(f'Best: {best_node}')
            # print(f'Len of Q: {len(Q)}')
            most_promising = Q.pop(0)
            for child in most_promising.get_children():
                # print(child)
                if child.has_better_value(best_node):
                    best_node = child
                # If no complete solution yet, track the most promising one (by bound)
                elif best_node is None or len(best_node.tour) != len(self.distance_matrix):
                    if child.might_be_better_than(best_node):
                        best_node = child
                
                if child.might_be_better_than(best_node):
                    # print(f'    might be better than')
                    insort(Q, child) # uses __lt__ to sort

        named_tour = [self.cities[i] for i in best_node.tour]
        return f'{best_node.get_value()}\n{','.join(named_tour)}'


def main():
    file_path = sys.argv[1]
    solver = BranchAndBoundSolver(file_path)
    # print(solver)
    result = solver.find_solution()
    print(result)

if __name__ == '__main__':
    main()