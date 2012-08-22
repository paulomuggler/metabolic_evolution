import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time



class Control(nx.DiGraph):
    def __init__(self, genes, p):
        nx.DiGraph.__init__(self)
        self.number_genes = genes
        self.landscape = nx.DiGraph()
        self.p = p
        self.switch_dict = {}
        self.generate_random()
   

        
    def generate_random(self):
        #CUIDADO!!!! A numeracao tem que ser correspondente aos nos das reacoes na outra classe!!!!
        for gene1 in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.add_node(gene1,  {'on': r,'Next': r})
            for gene2 in range(self.number_genes):
                if rndm.random() <= self.p:
                    w = 2*(rndm.randint(0,1)-0.5)
                    self.add_edge(gene1, gene2, {'w': w})


    def change_state(self):
        threshold = 0
        self.switch_dict = {}
        gene_string = []
        for n in self.nodes():
            signal = 0
            control_nodes = self.predecessors(n)
            for cn in control_nodes:
                signal += self.edge[cn][n]['w']*self.node[cn]['on']
            if signal > threshold:
                if self.node[n]['on'] == False:
                    self.node[n]['Next'] = True
                    self.switch_dict.update({n:True})
                
            else:
                if self.node[n]['on'] == True:
                    self.node[n]['Next'] = False
                    self.switch_dict.update({n:False})
        for n in self.nodes():
            self.node[n]['on'] = self.node[n]['Next']
            gene_string.append(self.node[n]['on'] + 0)
     
        return gene_string

    def reset_random(self):
        for g in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.node[g]['on'] = r
            

    def set_configuration(self, config):
        b = bin(config)
        lis_b = [int(x) for x in b[2:]]
        lis_b.reverse()        
        lis_b.extend([0]*(self.number_genes - len(lis_b)))
        for g in range(self.number_genes):
            self.node[g]['on'] = (True == lis_b[g])

    def draw_landscape(self):
        for config in range(2**self.number_genes):
            self.landscape.add_node(bin(config))
        for config in range(2**self.number_genes):
            self.set_configuration(config)
            next_config = self.change_state()
            next_config.reverse()
            bla = [str(x) for x in next_config]
            bina = '0b' + ''.join(bla)
            self.landscape.add_edge(bin(config), bina)

        nx.draw_graphviz(self.landscape)
        plt.show()
        
##        pos_land = nx.pydot_layout(self.landscape)
##        plt.draw()
##        nx.draw_networkx_nodes(self.landscape,pos_land,node_size=150)
##        nx.draw_networkx_edges(self.landscape,pos_land,alpha=0.3)
##        plt.draw()
##        plt.clf()
##        nx.draw_networkx_nodes(self.landscape,pos_land,node_size=150)
##        nx.draw_networkx_edges(self.landscape,pos_land,alpha=0.3)
##        plt.draw()
        
        
        

a = Control(7,0.6)

a.draw_landscape()
