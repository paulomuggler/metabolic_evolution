import networkx as nx
import matplotlib.pyplot as plt
import random as rndm


class Organism(object):
    def __init__(self, nodes, p):

        organism = nx.fast_gnp_random_graph(nodes,p,directed=True)

        for node_origin in organism.nodes():
            organism.node[node_origin]=rndm.randint(0,1)
            for node_destiny in organism.edge[node_origin]:
                organism.edge[node_origin][node_destiny]['w'] = 2*(rndm.randint(0,1)-0.5)

        print 'nodes:'
        print organism.node

        print 'edges:'
        print organism.edge

        nx.draw_circular(organism)
        plt.show()

#a = Organism(11, 0.3)

        
