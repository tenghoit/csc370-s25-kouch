import random

def promising(i, col):
    """
    Check if the queen placed at row i (with column col[i])
    does not conflict with any queen in previous rows.
    """
    for k in range(i):
        # Check same column or diagonal conflicts.
        if col[k] == col[i] or abs(col[k] - col[i]) == i - k:
            return False
    return True

def estimate_n_queens(n):
    # We use a list of length n to represent column positions for rows 0 to n-1.
    col = [0] * n  
    i = 0
    numnodes = 1
    m = 1
    mprod = 1

    while m != 0 and i != n:
        mprod = mprod * m
        numnodes = numnodes + mprod * n
        i += 1  # Move to the next row.
        m = 0
        prom_children = []  # This will store the candidate columns for row i.

        # Try each column j for the current row i.
        for j in range(n):  # j goes from 0 to n-1 (equivalent to 1..n in pseudocode)
            col[i-1] = j  # Temporarily assign column j to row i-1 (since i was incremented)
            if promising(i-1, col):
                m += 1
                prom_children.append(j)

        if m != 0:
            # Randomly select one of the promising children for row i-1.
            j = random.choice(prom_children)
            col[i-1] = j

    return numnodes

# Example usage:
if __name__ == "__main__":
    n = 8

    results = []

    for i in range(20):
        nodes_estimate = estimate_n_queens(n)
        results.append(nodes_estimate)
        print("Estimated number of nodes for n =", n, "is", nodes_estimate)

    average = sum(results)/len(results)

    print(f'AVG: {average}')
