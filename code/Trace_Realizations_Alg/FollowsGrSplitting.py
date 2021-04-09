import networkx as nx
from Trace_Realizations_Alg.combine_With_swapping import combine_With_swapping
from Trace_Realizations_Alg.IntervalGrSplitting import IntervalGrSplitting

def FollowsGrSplitting(E, FG, IG, V):

    if len(V) == 1:
        v = V[0]
        return [[v]]
    subgraph = nx.subgraph(FG, V)

    # need the undirected variant of the subgraph for the component function
    G = nx.to_undirected(subgraph)
    components = list(nx.connected_components(G))

    Pi_lists = []
    # each component is a set of nodes
    for component in components:
        C = list(component)
        Pi = IntervalGrSplitting(E, FG, IG, C)
        Pi_lists.append(Pi)

    sequences = combine_With_swapping(Pi_lists)

    return sequences