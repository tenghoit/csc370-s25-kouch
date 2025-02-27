import random


def terary(num: int) -> str:

    if num == 0: return '0'

    result = ''

    while num > 0:
        result = str(num % 3) + result
        num = num // 3

    return result


def get_difference(input_set: list[int], permutation: str) -> list[list[list[int]], int]:

    subsets = [[], [], []]

    for index in range(len(permutation)):
        group = int(permutation[index])
        subsets[group].append(input_set[index])

    set1_sum = sum(subsets[0])
    set2_sum = sum(subsets[1])
    set3_sum = sum(subsets[2])

    difference = abs(set1_sum - set2_sum) + abs(set2_sum - set3_sum) + abs(set3_sum - set1_sum)

    return [subsets, difference]


def brute_force(input_set: list[int]) -> list[list[list[int]], int]:
    """

    A brute force algorithm is one that explores all possible permutation in order to find the best solution.
    It's usually simple, but takes a long time.

    This algorithm is an example of a brute force because:
     - it generate all possible permutations using a ternary system (each int can be in 1 of the 3 subsets)
     - compare each permutation to see if it's the best currently

    """

    num_input = len(input_set)

    max_permutations = pow(3, num_input)

    inital_permutation = ''.zfill(num_input)
    best_permutation = get_difference(input_set, inital_permutation)

    for i in range(max_permutations):

        terary_str = terary(i).zfill(num_input)

        result = get_difference(input_set, terary_str)

        if result[1] < best_permutation[1]:
            best_permutation[0] = result[0]
            best_permutation[1] = result[1]

        print(f'Permutation: {result[0]} | Difference: {result[1]}')

    
    return best_permutation





def greedy(input_set: list[int]) -> list[list[list[int]], int]:
    """

    A greedy algorithm is one that trys to find an optimal solution by doing what makes the most sense currently.
    It does not guaranntee an optimal solution, but runs much faster than brute-force.

    This algorithm is an example of a greedy alogorithm because:
     - sorts the list so that largest int go first
     - put new value into the subset with lowest sum (no looking ahead)
     - essentially, each iteration trys to minimize difference


    Here is an instance where greedy fails to find the optimal solution:

        Input: [31, 53, 43, 58, 57, 64, 77, 29, 32, 9]

        Brute Force
        Permutation: [[31, 43, 77], [53, 57, 32, 9], [58, 64, 29]] | Difference: 0

        Greedy
        Permutation: [[77, 43, 29], [64, 53, 31], [58, 57, 32, 9]] | Difference: 16


    """
    input_set = reversed(sorted(input_set))

    result = [[], [], []]

    for value in input_set:
        sums = [sum(result[0]), sum(result[1]), sum(result[2])]

        min_index = sums.index(min(sums))

        result[min_index].append(value)

    set1_sum = sum(result[0])
    set2_sum = sum(result[1])
    set3_sum = sum(result[2])

    difference = abs(set1_sum - set2_sum) + abs(set2_sum - set3_sum) + abs(set3_sum - set1_sum)
    return [result, difference]




def main():
    count = 10
    max_range = 100
    input_set = random.sample(range(1,max_range), count)
    print(f'Input: {input_set}')

    bf = brute_force(input_set)
    print(f'\nInput: {input_set}')
    print('\nBrute Force')
    print(f'Permutation: {bf[0]} | Difference: {bf[1]}')
    gf = greedy(input_set)
    print('\nGreedy')
    print(f'Permutation: {gf[0]} | Difference: {gf[1]}')


if __name__ == '__main__':
    main()