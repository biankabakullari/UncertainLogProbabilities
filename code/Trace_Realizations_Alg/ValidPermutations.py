import networkx as nx
from Trace_Realizations_Alg.FollowsGraph import FollowsGraph
from Trace_Realizations_Alg.FollowsGrSplitting import FollowsGrSplitting

def ValidPermutations(E):
    # build Follows Graph
    FG = FollowsGraph(E)
    # build undirected variant of FG (=Comparability graph)
    G = nx.to_undirected(FG)
    # build complement graph (=Interval Graph)
    IG = nx.complement(G)

    V = list(FG.nodes)
    Re = FollowsGrSplitting(E, FG, IG, V)
    Re_clean = []
    for sequence in Re:
        s = [x[0] for x in sequence]
        Re_clean.append(s)
    return Re_clean