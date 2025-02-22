import sys


class Item:
    def __init__(self, item_name: str, item_weight: int, item_value: int) -> None:
        self.item_name = item_name
        self.item_weight: int = item_weight
        self.item_value: int = item_value

    def print(self):
        print(f'Item Name: {self.item_name} | Item Weight: {self.item_weight} | Item Value: {self.item_value}')



def main():
    
    if len(sys.argv) != 5:
        print('Invalid Args Count')
        exit()


    max_items = int(sys.argv[1])
    weight_limit = int(sys.argv[2])
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    # print(max_items, weight_limit, input_file_name, output_file_name)

    items = []

    # get items
    with open(input_file_name, 'r') as file:

        for i in range(max_items):

            item_name = file.readline()

            if item_name == "":
                break

            item_weight = int(file.readline())
            item_value = int(file.readline())

            items.append(Item(item_name, item_weight, item_value))

    num_items = len(items)

    # for item in items: item.print()
    # # print(f'Num Items: {num_items}')

    max_number_of_permutations = pow(2, num_items)
    # print(f'Num Permutations: {max_number_of_permutations}')

    optimal_permutation = ["", 0, 0]

    with open(output_file_name, 'w') as output:
        
        # going all permutations
        for i in range(0b0, max_number_of_permutations):
            binary_str = bin(i)[2:].zfill(num_items) # convert to str and add 0s
            binary_str = binary_str[::-1] # reverse
            # print(binary_str)
            
            total_weight = 0
            total_value = 0

            # getting weights and values
            for index in range(num_items):
                if binary_str[index] == '0':
                    continue

                total_weight += items[index].item_weight
                total_value += items[index].item_value


            # check if new optimal
            if total_value > optimal_permutation[2]:

                if total_weight <= weight_limit:
                    optimal_permutation[0] = binary_str
                    optimal_permutation[1] = total_weight
                    optimal_permutation[2] = total_value

            # print(total_weight)
            # print(total_value)

            output.write(f'{binary_str}\n{total_weight}\n{total_value}\n')

        
        output.write(f'{optimal_permutation[0]}\n{optimal_permutation[1]}\n{optimal_permutation[2]}')
        # print(optimal_permutation)




if __name__ == '__main__':
    main()