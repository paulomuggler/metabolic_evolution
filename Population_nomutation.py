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
reac = 50
gen = 50
p = 0.2
pop_size = 100
division_threshold = 50
record_size = 10
rate = 0
number_environments = 2

ta = 100
tb = 100

MetNet = None

#O ambiente eh gerado antes de mais nada!!!
#Aqui tem que ser decidido sobre as condicoes.

##environ_list = [[True]*food]
##for e in range(number_environments - 1):
##    environ_list.append([(1 == rndm.randint(0,1)) for i in range(food)])


class Population():
    def __init__(self):
        self.time = 0
        self.records = ['a']*record_size
        self.worst_record = 'a'
        self.population = [None]*pop_size
        for o in range(pop_size):
            self.population[o] = Organism(MetNet, met, reac, food, targets, gen, p, True)
            self.population[o].species = o
        
    def step(self):
        #da um passo na rede booleana e atualiza os estados das reacoes quimicas
        #e incrementa/decrementa a biomassa de cada individuo da populacao

        if self.time%tb == 0:
            self.genometofile()
            
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
            self.population[-1].species = self.population[o].species
            fobj = open('divide0.txt', 'a')
            fobj.write('dividiu: ' + str(o) + ' da especie: ' + str(self.population[o].species) + ' com a idade ' + str(self.population[o].age) + '\n')
            fobj.close()
            

 
        
            if self.population[o].age < self.population[o].record:
                self.population[o].record = self.population[o].age
            
            
            if self.population[o].age < self.worst_record:
                self.records.append(self.population[o].age)
                self.records.sort()
                self.records.pop()
                self.worst_record = self.records[-1]
                print 'records!'
                fobj = open('records0.txt', 'a')
                fobj.write('records:' + str(self.records))
                fobj.write('\n+++++++++++++++++++++++++++\n')
                fobj.write(str(self.population[o].control.edges()))
                fobj.write('\n+++++++++++++++++++++++++++\n')
                fobj.close()


            self.population[o].age = 0
            self.population[o].biomass = 0

        popping_list = sorted(rndm.sample(range(len(self.population)), len(lista_o)))
        print 'divide!'
        fobj = open('divide0.txt', 'a')
        fobj.write('popping: ' + str(popping_list))
        

        decr = 0
        for d in popping_list:
            self.population.pop(d + decr)
            decr -= 1
        fobj.write('\ndivision ages:\n' + str([self.population[ind].record for ind in range(pop_size)]))
        fobj.write('\nmothers ages:\n' + str([self.population[ind].mother_record for ind in range(pop_size)]) + '\n\n')
        fobj.close()

        fobj = open('species0.txt', 'a')
        fobj.write(str([self.population[ind].species for ind in range(pop_size)]) + '\n')
        fobj.close()

    def genometofile(self):
        fobj = open('genome0.txt', 'a')
        fobj.write('timestep: ' + str(self.time) + '\n')
        r = 'a'
        ix = 0
        for i in range(pop_size):
            if self.population[i].record < r:
                r = self.population[i].record
                ix = i
        fobj.write('division age: ' + str(r) + '\n')
        fobj.write('DNA: ' + '\n' + str(self.population[ix].control.export_code()) + '\n' )
        fobj.write('control: ' + '\n' + str(self.population[ix].control.edges()) + '\n' )
        fobj.write('on/off: ' + '\n' + str([self.population[ix].control.node[n]['on'] for n in self.population[ix].control.nodes()]) + '\n')
        fobj.write('# - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # \n\n')
        fobj.close()

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

def calculamedia(listaas):
    n = 0
    media = 0.0
    for el in listaas:
        if el == 'a':
            continue
        media += el
        n += 1
    return media/n

def headertofile(string):

    fobj = open('header0.txt', 'a')
    fobj.write(string)
    fobj.write('\n\n' + 'food = ' + str(food))
    fobj.write('\n' + 'targets = ' + str(targets))
    fobj.write('\n' + 'met = ' + str(met))
    fobj.write('\n' + 'reac = ' + str(reac))
    fobj.write('\n' + 'gen = ' + str(gen))
    fobj.write('\n' + 'p = ' + str(p))
    fobj.write('\n' + 'pop_size = ' + str(pop_size))
    fobj.write('\n' + 'division_threshold = ' + str(division_threshold))
    fobj.write('\n' + 'record_size = ' + str(record_size))
    fobj.write('\n' + 'rate = ' + str(rate))
    fobj.write('\n' + 'number_environments = ' + str(number_environments))
    fobj.write('\n' + 'ta = ' + str(ta))
    fobj.write('\n' + 'tb = ' + str(tb))
    fobj.close()


def monitormutation():     
    food_total = 10
    reac_total = 70
    metabolites = 80
    food = 8
    reac = 20
    targets = 1
    p = 0.2
    rate = 0.0005

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
    print 'father control: ' + str(fathers_list[0].control.edges())
    print 'son control: ' + str(descendent_list[0].control.edges())
    print 'father genes: ' + str([fathers_list[0].control.node[n]['on'] for n in fathers_list[0].control.nodes()])
    print 'son genes: ' + str([descendent_list[0].control.node[n]['on'] for n in descendent_list[0].control.nodes()])
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

def constant_size_environment_random():

    headertofile('constant_size_environment_random')

    global MetNet

    environ_list = [[True]*food]
    for e in range(number_environments - 1):
        environ_list.append([(1 == rndm.randint(0,1)) for i in range(food)])

    print 'environment!'
    fobj = open('environment0.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(met, reac, food, targets, environ_list)

    
    fobj = open('MetNet0.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
    
    a = Population()
    division = []
    env_change_rate = 0.02
    chg = False

    media_idades_reprod = []

    while True:
        a.step()
        

            
        if rndm.random() < env_change_rate:
            chg = True
            env_ind = rndm.randint(0,number_environments - 1)
        for o in range(pop_size):
            if chg:
                a.population[o].change_environment_org(environ_list[env_ind])
                
            if a.population[o].biomass > division_threshold:
                division.append(o)
        if len(division) > 0:
            a.divide(division, rate, MetNet)
            division = []

        if a.time%ta == 0:
            media_idades_reprod.append(calculamedia([a.population[ind].mother_record for ind in range(pop_size)]))
            print 'media_idades'
            fobj = open('media_idades0.txt', 'a')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        
        chg = False

def constant_size_environment_periodic():

    headertofile('constant_size_environment_periodic')

    global MetNet

    envchg_period = 100

    environ_list = [[True]*(food/2) + [False]*(food - food/2),[False]*(food/2) + [True]*(food - food/2)]

    print 'environment!'
    fobj = open('environment0.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(met, reac, food, targets, environ_list)

    fobj = open('MetNet0.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 
    
    a = Population()
    division = []
    chg = False
    env_ind = 0

    media_idades_reprod = []

    while True:
        a.step()
        

            
        if a.time%envchg_period == 0:
            chg = True
            env_ind = (env_ind + 1)%2
        for o in range(pop_size):
            if chg:
                a.population[o].change_environment_org(environ_list[env_ind])
                
            if a.population[o].biomass > division_threshold:
                division.append(o)
        if len(division) > 0:
            a.divide(division, rate, MetNet)
            division = []

        if a.time%ta == 0:
            media_idades_reprod.append(calculamedia([a.population[ind].mother_record for ind in range(pop_size)]))
            print 'media_idades'
            fobj = open('media_idades0.txt', 'a')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        
        chg = False          

def constant_size_environment_periodic_3():

    headertofile('constant_size_environment_periodic_3')

    global MetNet

    envchg_period = 100

    environ_list = [[True]*(food/3) + [False]*(food - food/3),[False]*(food/3) + [True]*(food/3) + [False]*(food - 2*(food/3)), [False]*(2*(food/3))+ [True]*(food - 2*(food/3))]

    print 'environment!'
    fobj = open('environment0.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(met, reac, food, targets, environ_list)

    fobj = open('MetNet0.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 
    
    a = Population()
    division = []
    chg = False
    env_ind = 0

    media_idades_reprod = []

    while True:
        a.step()
        

            
        if a.time%envchg_period == 0:
            chg = True
            env_ind = (env_ind + 1)%3
        for o in range(pop_size):
            if chg:
                a.population[o].change_environment_org(environ_list[env_ind])
                
            if a.population[o].biomass > division_threshold:
                division.append(o)
        if len(division) > 0:
            a.divide(division, rate, MetNet)
            division = []

        if a.time%ta == 0:
            media_idades_reprod.append(calculamedia([a.population[ind].mother_record for ind in range(pop_size)]))
            print 'media_idades'
            fobj = open('media_idades0.txt', 'a')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        
        chg = False 
            
def constant_size_environment_constant():

    headertofile('constant_size_environment_constant')

    global MetNet

    environ_list = [[True]*food]

    print 'environment!'
    fobj = open('environment0.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(met, reac, food, targets, environ_list)

    fobj = open('MetNet0.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 

    a = Population()
    division = []

    media_idades_reprod = []

    while True:
        a.step()
        

        for o in range(pop_size):                
            if a.population[o].biomass > division_threshold:
                division.append(o)
        if len(division) > 0:
            a.divide(division, rate, MetNet)
            division = []

        if a.time%ta == 0:
            media_idades_reprod.append(calculamedia([a.population[ind].mother_record for ind in range(pop_size)]))
            print 'media_idades'
            fobj = open('media_idades0.txt', 'w')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        

##monitormutation()
##constant_size_population()
##growing_descendents()
##constant_size_environment_random()
##constant_size_environment_periodic()
##constant_size_environment_periodic_3()
constant_size_environment_constant()
