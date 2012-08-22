import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from copy import deepcopy

gray = "#C0C0C0"
green = "#00FF00"

palette = []


palette.append(gray)
palette.append(green)


plt.ion()

class Control(nx.DiGraph):
    def __init__(self, food_total, metabolites, genes_list, p, reac_total, inicial = False, DNA = None, mother = None):

        # Essa lista de genes ja tem que ser uma lista
        #nao repetida de chaves (hashable), incluindo todas as food molecules
        #quando da criacao de um novo organismo. Essa lista vem vazia
        #num organismo derivado da importacao de um DNA.
        
        nx.DiGraph.__init__(self)
        #Tomar cuidado se for colocar soh parte das food molecules, muitas coisas dependem disso!
        self.number_food_total = food_total
        self.number_metabolites = metabolites
        self.number_reac_total = reac_total
        
        #SERA QUE ESSA COPIA PRECISARIA SER DEEP?
        
        self.switch_dict = {}
        self.colors = []         
       
        if inicial:
            self.p = p
            self.genes_list = genes_list
            #nessa genes_list ja ta incluida a lista de food molecules
            #cuidado! Nao existe uma verificacao
            #por chaves repetidas nessa lista!!
            
            self.number_food_actual = len([f for f in self.genes_list if f in range(self.number_food_total)])            
            self.number_genes = len(genes_list)
            self.generate_minimum()
##            self.generate_random()
        else:
            self.genes_list = []
            self.import_code(DNA, mother)
            self.number_food_actual = len([f for f in self.genes_list if f in range(self.number_food_total)])
            
        

    def generate_minimum(self):
        
        #ele gera a topologia (com pesos) e ja seta os ligados/desligados iniciais.
        for gene in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.add_node(self.genes_list[gene],  {'on': r or (gene in range(self.number_food_total)),'Next': r or (gene in range(self.number_food_total))})
            if gene not in range(self.number_food_total):
                self.add_edge(self.genes_list[gene], self.genes_list[gene], {'w': 2*(rndm.randint(0,1)-0.5)})
            self.colors.append(palette[(r or (gene in range(self.number_food_total))) + 0])
            if r and (gene not in range(self.number_food_total)): #or (gene1 in range(self.number_food_total)):
                self.switch_dict.update({self.genes_list[gene]:True})
        
        pos2 = nx.circular_layout(self)
        self.pos = {}
        for i in self.genes_list:
            self.pos[i] = pos2[self.nodes()[self.genes_list.index(i)]]

##        self.draw_BN(self.pos, self.genes_list)    #Na falta de alternativa melhor, desenha-se duas vezes para funcionar.
        self.draw_BN(self.pos, self.genes_list)

        
    def generate_random(self):
        
        #ele gera a topologia (com pesos) e ja seta os ligados/desligados iniciais.
        for gene1 in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.add_node(self.genes_list[gene1],  {'on': r or (gene1 in range(self.number_food_total)),'Next': r or (gene1 in range(self.number_food_total))})
            self.colors.append(palette[(r or (gene1 in range(self.number_food_total))) + 0])
            if r and (gene1 not in range(self.number_food_total)): #or (gene1 in range(self.number_food_total)):
                self.switch_dict.update({self.genes_list[gene1]:True})
                print 'generate_random ' + str(self.genes_list[gene1])

            for gene2 in range(self.number_genes - self.number_food_actual):
                if rndm.random() <= self.p:
                    w = 2*(rndm.randint(0,1)-0.5)
                    self.add_edge(self.genes_list[gene1], self.genes_list[gene2 + self.number_food_actual], {'w': w})
        
        
        pos2 = nx.circular_layout(self)
        self.pos = {}
        for i in self.genes_list:
            self.pos[i] = pos2[self.nodes()[self.genes_list.index(i)]]

        self.draw_BN(self.pos, self.genes_list)    #Na falta de alternativa melhor, desenha-se duas vezes para funcionar.
        self.draw_BN(self.pos, self.genes_list)

        

    def change_state(self):
        # Da um passo na configuracao on/off dos genes
        threshold = 0
        self.switch_dict = {}
        self.food_dict = {}
        gene_string = []


        for n in self.nodes():
            if n in range(self.number_food_total):
                continue
            signal = 0
            control_nodes = self.predecessors(n)
            for cn in control_nodes:
                signal += self.edge[cn][n]['w']*self.node[cn]['on']
            if signal > threshold:
                if self.node[n]['on'] == False:
                    self.node[n]['Next'] = True
                    self.switch_dict.update({n:True})
##                    print 'change_state_1 ' + str(n)                                        
                
            else:
                if self.node[n]['on'] == True:
                    self.node[n]['Next'] = False
                    self.switch_dict.update({n:False})
##                    print 'change_state_2 ' + str(n)


#SERA QUE NAO FUNCIONA?!?
                    
        for n in range(self.number_genes):                                                 
            self.node[self.genes_list[n]]['on'] = self.node[self.genes_list[n]]['Next']
            self.colors[n] = palette[self.node[self.genes_list[n]]['on'] + 0]
            gene_string.append(self.node[self.genes_list[n]]['on'] + 0)


##        for n in self.switch_dict:
##            self.node[n]['on'] = self.node[n]['Next']
##            self.colors[self.genes_list.index(n)] = palette[self.node[n]['on'] + 0]
##            gene_string.append(self.node[n]['on'] + 0)


        self.draw_BN(self.pos, self.genes_list)

        #print self.nodes()
        
        return gene_string

    def reset_random(self):
        gene_string = []
        self.switch_dict ={}
        
        
        for g in range(self.number_genes):
            if g in range(self.number_food_actual):
                continue
            r = (True == rndm.randint(0,1))
            self.node[self.genes_list[g]]['on'] = r
            self.switch_dict.update({self.genes_list[g]:r})
            self.colors[g] = palette[self.node[self.genes_list[g]]['on'] + 0]
            gene_string.append(self.node[self.genes_list[g]]['on'] + 0)

        self.draw_BN(self.pos, self.genes_list)

    def export_code(self):
        pot_cn = (self.number_food_total + self.number_reac_total)
        K = self.number_food_total*pot_cn

        DNA = [0]*(pot_cn**2 - K)
        for a, b in self.edges():
            aa = a if a in range(self.number_food_total) else a - self.number_metabolites + self.number_food_total
            bb = b if b in range(self.number_food_total) else b - self.number_metabolites + self.number_food_total
            DNA[bb*pot_cn + aa - K] = self.edge[a][b]['w']
        return DNA
        
    def import_code(self, DNA, mother = None):
        #As geracoes mutadas ja nao terao mais nodes no controle de food molecules se elas nao estiverem conectadas a nada... 
        pot_cn = (self.number_food_total + self.number_reac_total)
        K = self.number_food_total*pot_cn
       
        for index in (i for i in xrange(len(DNA)) if abs(DNA[i]) == 1):
            a = (index + K)%pot_cn
            b = (index + K - a)/pot_cn
            aa = a if a in range(self.number_food_total) else a + self.number_metabolites - self.number_food_total
            bb = b if b in range(self.number_food_total) else b + self.number_metabolites - self.number_food_total
            self.add_edge(aa, bb, {'w': DNA[index]})
     

        
        
        for f in range(self.number_food_total):
            if f not in self.nodes():
                self.add_node(f)
                
        self.genes_list = deepcopy(self.nodes())
        self.genes_list.sort()
        self.number_genes = len(self.genes_list)

        if mother is None:
            for n in self.genes_list:
                r = (True == rndm.randint(0,1))
                self.node[n] = {'on': r or (n in range(self.number_food_total)),'Next': r or (n in range(self.number_food_total))}
                if r and (n not in range(self.number_food_total)): # or (n in range(self.number_food_total)):
                    self.switch_dict.update({n: True})

                self.colors.append(palette[self.node[n]['on'] + 0])

        else:
            for n in self.genes_list:
                if n in mother.nodes():
                    self.node[n] = {'on': mother.node[n]['on'],'Next': mother.node[n]['on']}
                    if mother.node[n]['on'] and (n not in range(self.number_food_total)): # or (n in range(self.number_food_total)):
                        self.switch_dict.update({n: True})

                    self.colors.append(palette[self.node[n]['on'] + 0])
                else:
                    r = (True == rndm.randint(0,1))
                    self.node[n] = {'on': r,'Next': r}
                    if r and (n not in range(self.number_food_total)): # or (n in range(self.number_food_total)):
                        self.switch_dict.update({n: True})

                    self.colors.append(palette[self.node[n]['on'] + 0])
                    
            

        
     

        

        pos2 = nx.circular_layout(self)

        self.pos = {}
        for i in self.genes_list:
            self.pos[i] = pos2[self.nodes()[self.genes_list.index(i)]]  #Desembaralhar essa merda....


        self.draw_BN(self.pos, self.genes_list)    #Na falta de alternativa melhor, desenha-se duas vezes para funcionar.
        self.draw_BN(self.pos, self.genes_list)

    def mutate_DNA(code, rate):
        for i in range(len(code)):
            if rndm.random() <= rate:
                print 'DNA[i]'
                print code[i]
                code[i] = (code[i]%3 + 2*rndm.randint(0,1))%3 - 1
        return code

    def change_environment(self, food_list):
        #food_list tem que ter o comprimento do numero de food_total sempre!!
        #A posicao correspondente a molecula f deve conter True ou False,
        #dependendo da condicao de disponibilidade daquela food_molecule

        self.food_dict = {}
        
        for f in range(self.number_food_total):
            if food_list[f]:
                if f not in self.nodes():
                    self.add_node(f,  {'on': True,'Next': True})
                    self.food_dict.update({f: True})
                else:
                    if  not self.node[f]['on']:
                        self.node[f] = {'on': True,'Next': True}
                        self.food_dict.update({f: True})                        
            else:
                if f in self.nodes():
                    if self.node[f]['on']:
                        self.node[f] = {'on': False,'Next': False}
                        self.food_dict.update({f: False}) 

    def draw_BN(graph, positions, listadenos):

##        plt.clf()
##        nx.draw_networkx_labels(graph, positions)
##        nx.draw_networkx_nodes(graph,positions, nodelist = listadenos, node_color=graph.colors,node_size=150)
##        nx.draw_networkx_edges(graph,positions,alpha=0.3)
##        plt.draw()
##        plt.draw()
        pass
    
def randomenv():
    food_total = 10
    reac_total = 70
    metabolites = 80
    food = 4
    reac = 20
    targets = 1
    p = 0.1


    if targets + food > metabolites:
        print 'Tem numero errado...'

    react_list = [x + metabolites for x in range(reac_total)]
    food_list = range(food_total)
    genes_list = food_list + sorted(rndm.sample(react_list, reac))

    primeiragerac = Control(food_total, metabolites, genes_list, p, reac_total, inicial = True)
    
    dna = primeiragerac.export_code()
    time.sleep(5)
##    segundagerac = Control(food_total, metabolites, [], 0, reac_total, DNA = dna)
    segundagerac = Control(food_total, metabolites, [], 0, reac_total, DNA = dna, mother = primeiragerac) ##se a mae for indicada, o filho herda a configuracao

##
##    for t in range(6):
##        for i in range(50):
##            segundagerac.change_state()
##        segundagerac.change_environment([(1 == rndm.randint(0,1)) for i in range(food_total)])


##randomenv()
