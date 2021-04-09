from itertools import permutations
from Trace_Realizations_Alg.FollowsGraph import FollowsGraph

def NaivePermutations(E):
    # build Follows Graph
    FG = FollowsGraph(E)

    perms = permutations(FG.nodes)

    if len(E) == 1:
        return [E[0]]

    elif len(FG.edges) == 0:
        return permutations

    n = len(E)
    valid = []

    for p in perms:

        previous = []
        i = 0
        while i < n:
            event = p[i]
            if i == (n - 1):
                if event not in previous:
                    p_short = [node[0] for node in p]
                    valid.append(p_short)

            else:

                incoming_arcs = FG.in_edges(event)
                incoming_neighbors = [arc[0] for arc in incoming_arcs]

                if (i == 0 and len(incoming_arcs) > 0) or event in previous:
                    break
                else:
                    previous += incoming_neighbors

            i += 1

    return valid