import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from MetabolicNetwork import MetabolicNetwork
from Control import Control
from Organism import Organism
from copy import deepcopy


food = 20
targets = 1
met = 50
reac = 30
gen = 15
p = 0.2
pop_size = 50
division_threshold = 200
record_size = 10
rate = 0.001

MetNet = MetabolicNetwork(met, reac, food, targets)

class Population():
    def __init__(self):
        self.time = 0
        self.records = ['a']*record_size
        self.worst_record = 'a'
        self.population = [None]*pop_size
        for o in range(pop_size):
            self.population[o] = Organism(MetNet, met, reac, food, targets, gen, p, True)
        
    def step(self):
        #da um passo na rede booleana e atualiza os estados das reacoes quimicas
        #e incrementa/decrementa a biomassa de cada individuo da populacao
        for o in range(pop_size):
            genestr = self.population[o].control.change_state()
            self.population[o].chemistry.update_reactions(self.population[o].control.switch_dict)
            enzime_fraction = 0
            for j in range(len(genestr)- self.population[o].control.number_food_actual):
                enzime_fraction+=genestr[j + self.population[o].control.number_food_actual]
            enzime_fraction = float(enzime_fraction)/reac
            self.population[o].biomass = self.population[o].biomass + self.population[o].chemistry.path_to_target() - enzime_fraction
            self.population[o].age += 1
        self.time += 1
        
            
    def divide(self, lista_o, rate, MetNet):
        for o in lista_o:
            self.population.append(self.population[o].mutate(rate, MetNet))
            self.population[-1].mother_record = self.population[o].age
            print 'dividiu: ' + str(o) + ' com a idade ' + str(self.population[o].age) 
        
            if self.population[o].age < self.population[o].record:
                self.population[o].record = self.population[o].age
            
            
            if self.population[o].age < self.worst_record:
                self.records.append(self.population[o].age)
                self.records.sort()
                self.records.pop()
                self.worst_record = self.records[-1]
                print 'records: '
                print self.records

            self.population[o].age = 0
            self.population[o].biomass = 0

        popping_list = sorted(rndm.sample(range(len(self.population)), len(lista_o)))
        print 'popping: ' + str(popping_list)


        decr = 0
        for d in popping_list:
            self.population.pop(d + decr)
            decr -= 1
        print 'division ages: ' + str([self.population[ind].record for ind in range(pop_size)])
        print 'mothers ages: ' + str([self.population[ind].mother_record for ind in range(pop_size)])
        

def list_step(population, lista_o):
    for o in range(len(lista_o)):
        genestr = lista_o[o].control.change_state()
        lista_o[o].chemistry.update_reactions(lista_o[o].control.switch_dict)
        enzime_fraction = 0
        for j in range(len(genestr)- lista_o[o].control.number_food_actual):
            enzime_fraction+=genestr[j + lista_o[o].control.number_food_actual]
        enzime_fraction = float(enzime_fraction)/reac
        lista_o[o].biomass = lista_o[o].biomass + lista_o[o].chemistry.path_to_target() - enzime_fraction
        lista_o[o].age += 1
    population.time += 1
            
def mutate_DNA(code, rate):
    for i in range(len(code)):
        if rndm.random() <= rate:
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

def monitormutation():     
    food_total = 10
    reac_total = 70
    metabolites = 80
    food = 8
    reac = 20
    targets = 1
    p = 0.2
    rate = 0.0

    if targets + food > metabolites:
        print 'Tem numero errado...'

    react_list = [x + metabolites for x in range(reac_total)]
    food_list = sorted(rndm.sample(range(food_total), food))
    genes_list = food_list #+ sorted(rndm.sample(react_list, reac))


    primeira_geracao = Control(food_total, metabolites, genes_list, p, reac_total, inicial = True)
    dnap = primeira_geracao.export_code()
    dna = deepcopy(dnap)

    for j in range(50):

        print 'etapa' + str(j)
        gerac_um = Control(food_total, metabolites, [], 0, reac_total, DNA = dna)
        dna = mutate_DNA(dna, rate)
        time.sleep(0.5)


    dnamutante = crossover_DNA(dna, dnap, 2)
    gerac_mutante = Control(food_total, metabolites, [], 0, reac_total, DNA = dnamutante)


def constant_size_population():
    a = Population()
    division = []

    while True:
        a.step()
        for o in range(pop_size):
    ##        if a.population[o].biomass > 190:
    ##            print 'biomass ' + str(o) + ':' + str(a.population[o].biomass)
            if a.population[o].biomass > division_threshold:
                division.append(o)
        if len(division) > 0:
            print 'division: ' + str(division)
            a.divide(division, rate, MetNet)
            division = []
##        print 'tempo: ' + str(a.time)

def growing_descendents():
    fathers_list = []
    descendent_list = []
    division = []

    a = Population()
    while len(fathers_list) == 0:
        a.step()
        for o in range(pop_size):
            if a.population[o].biomass > division_threshold:
                fathers_list.append(a.population[o])
                descendent_list.append(a.population[o].mutate(rate, MetNet))
                a.population[o].biomass = 0
                a.population[o].age = 0
                print str(o) + ' appended!!'
                print 'tempo: ' + str(a.time)
    print fathers_list[0].control.edges()
    print descendent_list[0].control.edges()
    time.sleep(100)
    while True:
        list_step(a, descendent_list)
        list_step(a, fathers_list)
        for o in range(len(descendent_list)):
            if descendent_list[o].biomass > division_threshold:
                print 'filho dividiu com essa idade: ' + str(descendent_list[o].age)
                descendent_list[o].biomass = 0
                descendent_list[o].age = 0
        for o in range(len(fathers_list)):
            if fathers_list[o].biomass > division_threshold:
                print 'pai dividiu com essa idade: ' + str(fathers_list[o].age)
                fathers_list[o].biomass = 0
                fathers_list[o].age = 0

##        print 'tempo: ' + str(a.time)
        
        

##monitormutation()
constant_size_population()
##growing_descendents()
