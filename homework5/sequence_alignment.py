import sys
import csv

class DNA:
    def __init__(self, sequence1, sequence2, output_file_name):
        self.sequence1 = sequence1
        self.sequence2 = sequence2
        self.output_file_name = output_file_name
        self.num_rows = len(sequence1) + 1
        self.num_cols = len(sequence2) + 1

        self.table = [ [None for j in range(self.num_cols)] for i in range(self.num_rows)]

    def print_to_csv(self):
        with open(self.output_file_name, 'w') as file:
            writer = csv.writer(file)
            for row in self.table:
                writer.writerow(row)


    def opt(self, i: int, j: int):
        # print(f'Computing Row {i}, Col {j} ...')

        if self.table[i][j] is not None:
            return self.table[i][j]
        
        #base case for bot-right corner
        if i == self.num_rows - 1 and j == self.num_cols - 1: 
            self.table[i][j] = 0
            return 0
    
        if(i == self.num_rows - 1):
            self.table[i][j] = 2 * (self.num_cols - j - 1)
            return self.table[i][j]
        elif(j == self.num_cols - 1):
            self.table[i][j] =  2 * (self.num_rows - i - 1)
            return self.table[i][j]
        

        penalty = 0 if self.sequence1[i] == self.sequence2[j] else 1

        self.table[i][j] = min(
            self.opt(i + 1, j + 1) + penalty, 
            self.opt(i + 1, j) + 2, 
            self.opt(i, j+ 1) + 2
        )
        
        return self.table[i][j]
    

    def optimal_cost(self):
        self.opt(0, 0)
        self.print_to_csv()
        self.backtrack()
        print(self.table[0][0])
    
    def backtrack(self):

        i, j = 0, 0
        final_sequence1 = ''
        final_sequence2 = ''

        while i < self.num_rows - 1 or j < self.num_cols - 1:

            diagonal = float('inf')
            lower = float('inf')
            right = float('inf')

            # diagona
            if i < self.num_rows - 1 and j < self.num_cols - 1:
                penalty = 0 if self.sequence1[i] == self.sequence2[j] else 1
                diagonal = self.table[i + 1][j + 1] + penalty

            if i < self.num_rows - 1:
                lower = self.table[i + 1][j] + 2

            if j < self.num_cols - 1:
                right = self.table[i][j + 1] + 2

            if diagonal == self.table[i][j]:
                if penalty == 1:
                    final_sequence1 += f'[{self.sequence1[i]}]'
                    final_sequence2 += f'[{self.sequence2[j]}]'
                else:
                    final_sequence1 += f'{self.sequence1[i]}'
                    final_sequence2 += f'{self.sequence2[j]}'

                i += 1
                j += 1
            
            elif lower == self.table[i][j]:
                final_sequence1 += f'{self.sequence1[i]}'
                final_sequence2 += '-'
                i += 1
            elif right == self.table[i][j]:
                final_sequence1 += '-'
                final_sequence2 += f'{self.sequence2[j]}'
                j += 1


        while '][' in final_sequence1:
            final_sequence1 = final_sequence1.replace('][', '')

        while '][' in final_sequence2:
            final_sequence2 = final_sequence2.replace('][', '')


        print(final_sequence1)
        print(final_sequence2)

        



def main():

    if len(sys.argv) != 4:
        print(f'Incorrect Usage: python3 {sys.argv[0]} <sequence1.txt> <sequence2.txt> <table.csv>')

    sequence1 = ''
    sequence2 = ''

    with open(sys.argv[1], 'r') as file1:
        sequence1 = file1.readline().strip()

    with open(sys.argv[2], 'r') as file2:
        sequence2 = file2.readline().strip()


    axo = DNA(sequence1, sequence2, sys.argv[3])

    axo.optimal_cost()
    # print(axo.table)


if __name__ == '__main__':
    main()