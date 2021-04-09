#!/usr/bin/env python
# coding: utf-8

import networkx as nx

def FollowsGraph(E):
    
    #use the (ID, tmin) for the nodes --> keeping only the ID enables detecting identical graphs, tmin necessary for sorting
    nodes = [(event.ID,event.tmin) for event in E]
    #here we will save the pairs of event.IDs such that (u,v) iff tmax(u) y tmin(v)
    arcs = []
    E_dict = {}
    for event in E:
        #keys are natural numbers, values are event objects with attributes ID, tmin, tmax
        E_dict[event.ID] = event
        
    #a list that will help us sort the events, necessary for determining the arcs 
    L = []
    for event in E_dict.values():
        #first pos: whole object because we will need its ID later
        #second pos: timestamp value needed for sorting
        #third pos: type of timestamps needed for the direction of the arcs
        L.append((event, event.tmin, 'MIN'))
        L.append((event, event.tmax, 'MAX'))
    
    #sort events based on timestamp 
    L.sort(key = lambda e: e[1])
    
    finished = []
    i = 0
    while i < len(L):
        event = L[i][0] #event object
        ts_type = L[i][2] #type MIN or MAX
        if ts_type == 'MAX':
            finished.append((event.ID, event.tmin))
        elif finished != []:
            v = (event.ID,event.tmin)
            for u in finished:
                arcs.append((u,v)) 
        i += 1
    
    FG = nx.DiGraph()
    FG.add_nodes_from(nodes)
    FG.add_edges_from(arcs)
    
    return FG






        
    






