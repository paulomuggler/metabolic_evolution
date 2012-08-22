#! /usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm

def constructMetabNetwork(metabolites, reactions, p):
    
    metab = nx.bipartite_random_graph(metabolites,reactions,p,directed=True)
    pos = {}

    for i in xrange(metabolites):
        pos[i] = (0,i)
        if metab.in_degree(i)==0 and metab.out_degree(i)==0:
            if rndm.random()<0.5:
                metab.add_edge(i,rndm.randint(metabolites,metabolites+reactions-1))
            else:
                metab.add_edge(rndm.randint(metabolites,metabolites+reactions-1),i)

    for i in xrange(reactions):
        pos[i+metabolites] = (metabolites, float(i)*metabolites/reactions)
        if metab.in_degree(i+metabolites)==0:
            metab.add_edge(rndm.randint(0,metabolites-1),i+metabolites)
        if metab.out_degree(i+metabolites)==0:
            metab.add_edge(i+metabolites,rndm.randint(0,metabolites-1))


    nx.draw(metab, pos)
    plt.show()
    return metab

constructMetabNetwork(100,27,0.0001)
