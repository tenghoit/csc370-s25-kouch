# class Solution:

#     def __init__(self, input_set: set(int)) -> None:

#         self.input = input_set

#         self.set1 = []
#         self.set2 = []
#         self.set3 = []


#     def reset(self) -> None:
#         self.set1 = []
#         self.set2 = []
#         self.set3 = []

    
#     def get_difference(self) -> int:

#         set1_sum = sum(self.set1)
#         set2_sum = sum(self.set2)
#         set3_sum = sum(self.set3)

#         return abs(set1_sum - set2_sum) + abs(set2_sum - set3_sum) + abs(set3_sum - set1_sum)


#     def brute_force(self) -> None:
#         pass

def terary(num: int) -> str:

    if num == 0: return '0'

    result = ''

    while num > 0:
        result = str(num % 3) + result
        num = num // 3

    return result


def get_difference(input_set: list[int], permutation: str) -> int:

    subsets = [[], [], []]

    for index in range(len(permutation)):
        group = int(permutation[index])
        subsets[group].append(input_set[index])

    set1_sum = sum(subsets[0])
    set2_sum = sum(subsets[1])
    set3_sum = sum(subsets[2])

    print(subsets)

    return abs(set1_sum - set2_sum) + abs(set2_sum - set3_sum) + abs(set3_sum - set1_sum)



def brute_force(input_set: list[int]) -> None:

    num_input = len(input_set)

    max_permutations = pow(3, num_input)

    inital_permutation = ''.zfill(num_input)
    best_permutation = [inital_permutation, get_difference(input_set, inital_permutation)]

    for i in range(max_permutations):

        terary_str = terary(i).zfill(num_input)
        print(terary_str)

        difference = get_difference(input_set, terary_str)
        print(difference)

        if difference < best_permutation[1]:
            best_permutation[0] = terary_str
            best_permutation[1] = difference

    
    print(best_permutation)
    print(get_difference(input_set, best_permutation[0]))








def main():
    input_set = [1, 2, 3, 4, 5, 6]

    brute_force(input_set)




if __name__ == '__main__':
    main()