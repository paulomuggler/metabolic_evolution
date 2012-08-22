#! /usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm

class Metabolism(object):
    
    def __init__(self,metabolites, reactions, p):
        #We generate any metabolic bipartite graph here, eventually from a set of different generators
        self.metabolic_network = nx.bipartite_random_graph(metabolites,reactions,p,directed=True)
        pos = {}
        for i in xrange(metabolites):
            pos[i] = (0,i)
            if self.metabolic_network.in_degree(i)==0 and self.metabolic_network.out_degree(i)==0:
                if rndm.random()<0.5:
                    self.metabolic_network.add_edge(i,rndm.randint(metabolites,metabolites+reactions-1))
                else:
                    self.metabolic_network.add_edge(rndm.randint(metabolites,metabolites+reactions-1),i)

        for i in xrange(reactions):
            pos[i+metabolites] = (metabolites, float(i)*metabolites/reactions)
            if self.metabolic_network.in_degree(i+metabolites)==0:
                self.metabolic_network.add_edge(rndm.randint(0,metabolites-1),i+metabolites)
            if self.metabolic_network.out_degree(i+metabolites)==0:
                self.metabolic_network.add_edge(i+metabolites,rndm.randint(0,metabolites-1))


        nx.draw(self.metabolic_network, pos)
        plt.show()

meta = Metabolism(12,7,0.0001)
