import itertools as it

def combine_WO_swapping(Pi_lists):
    k = len(Pi_lists)
    if k == 1:
        # Input is [P], return P
        return Pi_lists[0]

        # input is [P1,...,Pk] with k > 1
    full_sequences = []

    # on position j, element [0,...,len(P_j)]
    Pi_indices = []
    for i in range(k):
        indices = [x for x in range(len(Pi_lists[i]))]
        Pi_indices.append(indices)

    cartesian_prod_indices = []
    # each element shows in pos j with sequence to take from P_j
    for element in it.product(*Pi_indices):
        cartesian_prod_indices.append(element)
        sequence = []
        for i, x in enumerate(element):
            sequence += Pi_lists[i][x]
        full_sequences.append(sequence)

    return full_sequences
