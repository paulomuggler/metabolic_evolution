import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time


gray = "#C0C0C0"
green = "#00FF00"

palette = []


palette.append(gray)
palette.append(green)


#w,h=plt.figaspect(1)
#plt.figure(figsize=(w,h))
plt.ion()

class Control(nx.DiGraph):
    def __init__(self, genes, p):
        nx.DiGraph.__init__(self)
        self.number_genes = genes
        self.p = p
        self.colors = []
        A = nx.Graph()
        A.add_nodes_from(range(genes))
        self.pos = nx.spring_layout(A)
        self.switch_dict = {}
        self.generate_random()
        #print self.node
        #nx.draw_circular(self)
        #plt.show()

        
    def generate_random(self):
        #CUIDADO!!!! A numeracao tem que ser correspondente aos nos das reacoes na outra classe!!!!
        for gene1 in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.add_node(gene1,  {'on': r,'Next': r})
            self.colors.append(palette[r + 0])
            #print 'palette:'
            #print palette[r+0]
            #print str(gene1) + ': ' + str(r)
            for gene2 in range(self.number_genes):
                if rndm.random() <= self.p:
                    w = 2*(rndm.randint(0,1)-0.5)
                    self.add_edge(gene1, gene2, {'w': w})
                    #print str(gene1) + ' -> ' + str(gene2) + ': ' + str(w)
                    
        #print 'nodes:'
        #print self.node

        #print 'edges:'
        #print self.edge

        #nx.draw_circular(self, node_color=colors)
        #plt.show()
        #pos=nx.circular_layout(self)
        nodes=nx.draw_networkx_nodes(self,self.pos,node_color=self.colors,node_size=150)
        edges=nx.draw_networkx_edges(self,self.pos,alpha=0.3)
        plt.draw()




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
            self.colors[n] = palette[self.node[n]['on'] + 0]
            gene_string.append(self.node[n]['on'] + 0)
        #plt.clf()
        #nx.draw_circular(self, node_color=colors)
        plt.clf()
        nx.draw_networkx_nodes(self,self.pos,node_color=self.colors,node_size=150)
        nx.draw_networkx_edges(self,self.pos,alpha=0.3)
        plt.draw()

        return gene_string

    def reset_random(self):
        for g in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.node[g]['on'] = r
            #print str(g) + ': ' + str(r)
        
        

a = Control(50,0.05)


for j in range(10):
    print 'etapa' + str(j) 
    for i in range(50):
        a.change_state()
        a.reset_random()
