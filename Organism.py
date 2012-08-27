import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from MetabolicNetwork import MetabolicNetwork
from Control import Control
from copy import deepcopy

class GeneNumberException(Exception):
    pass


class Organism(nx.DiGraph):
    def __init__(self, MetNet, met, reac, number_food, targets, gen, p, inicial = False, control = None):
        #quais sao as caracteristicas em comum entre um organismo gerado from scratch
        #e um organismo proveninente de uma mutacao? Isso tem que estar no __init__
        
        #self.chemistry = MetNet

        self.age = 0
        self.record = 'a'
        self.mother_record = 'a'
        self.species = 'a'

        self.number_targets = targets
        food_list = range(number_food)
        
        if inicial: #verifica se a populacao eh inicial
            react_list = [x + met for x in range(MetNet.number_reactions)]
             

            if gen > len(react_list):
                raise GeneNumberException('There are more genes than reactions to be controlled!')

            genes_list = food_list + sorted(rndm.sample(react_list, gen))

            #talvez fosse util ter um dicionario que redireciona pra funcoes
            #dependendo do tipo de inicializacao - inicial ou mutacao - e
            #encapsular uma serie de coisas que por enquanto estao no __init__.

            self.chemistry = self.clean_met_net(MetNet, genes_list, food_list)
##            print 'o dicionario inicial de chemis:'
##            print self.chemistry.node
            self.control = Control(number_food, met, genes_list, p, reac, inicial)
##            print 'dicionario inicial:'
##            print self.control.switch_dict
            self.chemistry.update_reactions(self.control.switch_dict)
            self.biomass = 0
##            print 'biomass_init'
##            print self.biomass
        else: #caso a populacao seja gerada de uma mutacao...
            self.control = control
            self.chemistry = self.clean_met_net(MetNet, control.genes_list, food_list)
            self.chemistry.update_reactions(self.control.switch_dict)
            self.biomass = 0
            

    def clean_met_net(self, MetNet, genes_list, food_list):
        #Verificar com mais calma se a delecao de targets nao afeta nada...
        chemis = deepcopy(MetNet)
        #sera que esse objeto vai receber as funcoes da classe MetabolicNetwork?

        for r in [x for x in MetNet.nodes() if MetNet.node[x]['Type'] == 'R']:
            if r not in [reac for reac in genes_list if reac not in food_list]:
                chemis.remove_node(r)
        #Alguns targets podem ser deletados nesse passo:
        chemis.remove_nodes_from([isol for isol in nx.isolates(chemis) if isol not in food_list])

        #chemis.remove_nodes_from([n for n in nx.isolates(chemis) if n not in food_list])????
        #Talvez tenha que verificar se food ou target molecules foram removidos?
        return chemis
    
    def change_environment_org(self, food_list):
        self.control.change_environment(food_list)
        self.chemistry.update_food(self.control.food_dict)

    def mutate(self, rate, MetNet):

        DNAp = self.control.export_code()
        DNAm = mutate_DNA(DNAp, rate)
        control_son = Control(MetNet.number_food, MetNet.number_metabolites, [], 0, MetNet.number_reactions, DNA = DNAm, mother = self.control)
        
        return Organism(MetNet, MetNet.number_metabolites, MetNet.number_reactions, MetNet.number_food, MetNet.number_targets, 0, 0, inicial = False, control = control_son)

def mutate_DNA(code, rate):
    for i in range(len(code)):
        if rndm.random() < rate:
            code[i] = (code[i]%3 + 2*rndm.randint(0,1))%3 - 1
    return code

def crossover_DNA(codem, codep, number_points):
    coded = []
    points = rndm.sample(range(len(codem) - 1), number_points)
    dicdna = {0: codem, 1: codep}
    orig = rndm.randint(0,1)
    for i in xrange(len(codem)):
        coded.append(dicdna[orig][i])
        if i in points:
            orig = (orig + 1)%2
    return coded
        
def producedbiomass():        
    met = 50
    reac = 80
    food = 20
    targets = 1
    gen = 80
    p = 0.1
    rate = 1


    MetNet = MetabolicNetwork(met, reac, food, targets)
##    print 'o dicionario inicial de MetNet:'
##    print MetNet.node


    b = Organism(MetNet, met, reac, food, targets, gen, p, True)
    ts = []
##    b = c.mutate(rate, MetNet)
    a = b.mutate(rate, MetNet)
    print a.control.edges()

    print 'Biomassa:'
    print a.biomass
    ts.append(a.biomass)

    for t in range(20):

        for i in range(20):
            genestr = a.control.change_state()
##            print 'genestr: '
##            print genestr
            #print 'switch_dict: '
            #print a.control.switch_dict
            a.chemistry.update_reactions(a.control.switch_dict)
            enzime_fraction = 0 
            for j in range(len(genestr)- a.control.number_food_actual):
                enzime_fraction+=genestr[j + a.control.number_food_actual]
            enzime_fraction = float(enzime_fraction)/reac
##            print 'enzime_fraction: ' + str(enzime_fraction)
##            print 'a.chemistry.path_to_target: ' + str(a.chemistry.path_to_target())
            a.biomass = a.biomass + a.chemistry.path_to_target() - enzime_fraction
            print a.biomass
            ts.append(a.biomass)


##        a.change_environment_org([(1 == rndm.randint(0,1)) for i in range(food)])
##        a.control.reset_random()

    plt.figure(2)
    plt.plot(ts)
    plt.draw()
    plt.show()
    plt.draw()
    plt.show()



##producedbiomass()




