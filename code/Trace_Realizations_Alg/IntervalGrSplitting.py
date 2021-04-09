import networkx as nx
from Trace_Realizations_Alg.combine_WO_swapping import combine_WO_swapping
from Trace_Realizations_Alg.NaivePermutations import NaivePermutations

def IntervalGrSplitting(E, FG, IG, V):
    from Trace_Realizations_Alg.FollowsGrSplitting import FollowsGrSplitting

    if len(V) == 1:
        v = V[0]
        return [[v]]

    G = nx.subgraph(IG,V)
    components = list(nx.connected_components(G))

    if len(components) == 1:
        nodes = list(components[0])
        E_indices = [i for i in range(len(E)) for n in nodes if E[i].ID == n[0]]
        E_subset = [E[j] for j in E_indices]
        # print("Only 1 component!")
        naive = NaivePermutations(E_subset)
        sequences = []
        for sequence in naive:
            seq = [(sequence[i], E[j].tmin) for i in range(len(sequence)) for j in range(len(E)) if
                   E[j].ID == sequence[i]]
            sequences.append(seq)
        return [sequences]

    #help list to timely order the components
    L = []
    for component in components:
        C = list(component)
        start = min([tmin for (ID,tmin) in C])
        L.append((start, C))
    L.sort(key = lambda x: x[0])
    C_sorted = [l[1] for l in L]

    Pi_lists = []
    for C in C_sorted:
        #returns a list of sequences
        Pi = FollowsGrSplitting(E, FG, IG, C)
        Pi_lists.append(Pi)

    sequences = combine_WO_swapping(Pi_lists)

    return sequences