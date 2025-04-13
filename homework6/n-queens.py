n = 1
results = []

def is_promising(col):

    if len(col) < 2: return True

    end_index = len(col) - 1

    switch = True

    for i in range(len(col) - 1):
        if (col[i] == col[-1]) or (abs(col[i] - col[-1]) == end_index - i):
            switch = False

    return switch

def queens(col):
    
    if is_promising(col):

        if len(col) == n:
            results.append(col)
        else:
            for pos in range(n):
                new = col[:]
                new.append(pos)
                queens(new)



def estimate_n_queens(n):

    pass




while True:
    print(f'n: {n}')
    queens([])
    print(f'# Solutions: {len(results)}')
    n += 1
    results = []
