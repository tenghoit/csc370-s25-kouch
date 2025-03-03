import sys


class Item:
    def __init__(self, item_name: str, item_weight: int, item_value: int) -> None:
        self.item_name: str = item_name
        self.item_weight: int = item_weight
        self.item_value: int = item_value

    def print(self) -> None:
        print(f'Item Name: {self.item_name} | Item Weight: {self.item_weight} | Item Value: {self.item_value}')


def print_items(items: list[Item], result: list[Item]) -> None:

    for item in items:
        if item in result:
            print(f'{item.item_name}\n{item.item_weight}\n{item.item_value}')


def greedy_value(items: list[Item], weight_limit: int) -> None:

    items_sorted = sorted(items, key=lambda p: p.item_value)

    result = []
    current_weight = 0

    while len(items_sorted) > 0:

        item = items_sorted.pop()

        # print_items(items_sorted)
        # print()

        if(current_weight + item.item_weight > weight_limit):
            continue
        else:
            result.append(item)
            current_weight += item.item_weight

            # print(f'Current weight: {current_weight}')

    
    print_items(items, result)


def greedy_value_to_weight(items: list[Item], weight_limit: int) -> None:

    items_sorted = sorted(items, key=lambda p: (p.item_value / p.item_weight) )

    result = []
    current_weight = 0

    while len(items_sorted) > 0:

        item = items_sorted.pop()

        if(current_weight + item.item_weight > weight_limit):
            continue
        else:
            result.append(item)
            current_weight += item.item_weight

    
    print_items(items, result)


def main():

    # print(sys.argv)
    
    if len(sys.argv) != 5:
        print(f'Invalid Args Count: {len(sys.argv)} (Needs 5)')
        exit()

    max_items = int(sys.argv[1])
    weight_limit = int(sys.argv[2])
    heuristic_name = sys.argv[3]
    input_file_name = sys.argv[4]

    # print(max_items, weight_limit, heuristic_name, input_file_name)

    items = []

    # get items
    with open(input_file_name, 'r') as file:

        for i in range(max_items):

            item_name = file.readline().strip()

            if item_name == "":
                break

            item_weight = int(file.readline().strip())
            item_value = int(file.readline().strip())

            items.append(Item(item_name, item_weight, item_value))

    # print(f'Len of Items: {len(items)}')
    # print_items(items, items)
    # print()

    if heuristic_name == 'by_value':
        greedy_value(items, weight_limit)
    elif heuristic_name == 'value_to_weight':
        greedy_value_to_weight(items, weight_limit)



main()