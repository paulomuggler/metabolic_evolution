#!/usr/bin/python

import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from MetabolicNetwork import MetabolicNetwork
from Control import Control
from Organism import Organism
from Constants import Constants
from copy import deepcopy

#O ambiente eh gerado antes de mais nada!!!
#Aqui tem que ser decidido sobre as condicoes.



class Population():
    def __init__(self):
        self.time = 0
        self.records = ['a']*Constants.record_size
        self.worst_record = 'a'
        self.population = [None]*Constants.population_size
        for o in range(Constants.population_size):
            self.population[o] = Organism(MetNet, inicial = True)
            self.population[o].species = o
        
    def step(self):
        #da um passo na rede booleana e atualiza os estados das reacoes quimicas
        #e incrementa/decrementa a biomassa de cada individuo da populacao
        
        if self.time%Constants.tb == 0:
            self.genometofile()
            
        for o in range(Constants.population_size):
            genestr = self.population[o].control.change_state()
            self.population[o].chemistry.update_reactions(self.population[o].control.switch_dict)
            enzime_fraction = 0
            for j in range(len(genestr)- self.population[o].control.number_food_actual):
                enzime_fraction+=genestr[j + self.population[o].control.number_food_actual]
            enzime_fraction = Constants.peso*float(enzime_fraction)/(Constants.reactions + len(self.population[o].control.intermediate_list))
            self.population[o].biomass = self.population[o].biomass + self.population[o].chemistry.path_to_target() - enzime_fraction
            self.population[o].age += 1
        self.time += 1
        
            
    def divide(self, lista_o, rate, MetNet):
        for o in lista_o:
            self.population.append(self.population[o].mutate(rate, MetNet))
            self.population[-1].mother_record = self.population[o].age
            self.population[-1].species = self.population[o].species
            fobj = open(base_path+'divide.txt', 'a')
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
                fobj = open(base_path+'records.txt', 'a')
                fobj.write('records:' + str(self.records))
                fobj.write('\n+++++++++++++++++++++++++++\n')
                fobj.write(str(self.population[o].control.edges()))
                fobj.write('\n+++++++++++++++++++++++++++\n')
                fobj.close()


            self.population[o].age = 0
            self.population[o].biomass = 0

        popping_list = sorted(rndm.sample(range(len(self.population)), len(lista_o)))
        print 'divide!'
        fobj = open(base_path+'divide.txt', 'a')
        fobj.write('popping: ' + str(popping_list))
        

        decr = 0
        for d in popping_list:
            self.population.pop(d + decr)
            decr -= 1
        fobj.write('\ndivision ages:\n' + str([self.population[ind].record for ind in range(Constants.population_size)]))
        fobj.write('\nmothers ages:\n' + str([self.population[ind].mother_record for ind in range(Constants.population_size)]) + '\n\n')
        fobj.close()

        fobj = open(base_path+'species.txt', 'a')
        fobj.write(str([self.population[ind].species for ind in range(Constants.population_size)]) + '\n')
        fobj.close()

    def genometofile(self):
        fobj = open(base_path+'genome.txt', 'a')
        fobj.write('timestep: ' + str(self.time) + '\n')
        r = 'a'
        ix = 0
        for i in range(Constants.population_size):
            if self.population[i].record < r:
                r = self.population[i].record
                ix = i
        fobj.write('division age: ' + str(r) + '\n')
        fobj.write('DNA: ' + '\n' + str(self.population[ix].control.export_code()) + '\n' )
        fobj.write('control: ' + '\n' + str(self.population[ix].control.edges()) + '\n' )
        fobj.write('on/off: ' + '\n' + str([self.population[ix].control.node[n]['on'] for n in self.population[ix].control.nodes()]) + '\n')
        fobj.write('# - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # \n\n')
        fobj.close()
            
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
    if n == 0:
        return 0
    return media/n

def headertofile(string):

    fobj = open(base_path+'header.txt', 'a')
    fobj.write(string)
    fobj.write('\n\n' + 'food = ' + str(Constants.food))
    fobj.write('\n' + 'targets = ' + str(Constants.targets))
    fobj.write('\n' + 'metabolites = ' + str(Constants.metabolites))
    fobj.write('\n' + 'reactions = ' + str(Constants.reactions))
    fobj.write('\n' + 'genes = ' + str(Constants.genes))
    fobj.write('\n' + 'intermediate = ' + str(Constants.intermediate))
    fobj.write('\n' + 'p = ' + str(Constants.p))
    fobj.write('\n' + 'population_size = ' + str(Constants.population_size))
    fobj.write('\n' + 'division_threshold = ' + str(Constants.division_threshold))
    fobj.write('\n' + 'record_size = ' + str(Constants.record_size))
    fobj.write('\n' + 'rate = ' + str(Constants.rate))
    fobj.write('\n' + 'number_environments = ' + str(Constants.number_environments))
    fobj.write('\n' + 'envchg_period = ' + str(Constants.envchg_period))
    fobj.write('\n' + 'env_change_rate = ' + str(Constants.env_change_rate))
    fobj.write('\n' + 'peso = ' + str(Constants.peso))
    fobj.write('\n' + 'ta = ' + str(Constants.ta))
    fobj.write('\n' + 'tb = ' + str(Constants.tb))
    fobj.write('\n' + 'end_step = ' + str(Constants.end_step))
    fobj.close()

def constant_size(descriptive_string, environ_list, environ_change_method, period):
     
    headertofile(descriptive_string)
    global MetNet

    print 'environment!'
    fobj = open(base_path+'environment.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()

    MetNet = MetabolicNetwork(descriptive_string)

    fobj = open(base_path+'MetNet.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 

    a = Population()
    division = []
    chg = False
    env_ind = 0

    media_idades_reprod = []


    for my_step in xrange(Constants.end_step):
        a.step()

	chg, env_ind = environ_change_method(env_ind, period, a)

        for o in range(Constants.population_size):
            if chg:
                a.population[o].change_environment_org(environ_list[env_ind])
                
            if a.population[o].biomass > Constants.division_threshold:
                division.append(o)
        if len(division) > 0:
            a.divide(division, Constants.rate, MetNet)
            division = []

        if a.time%Constants.ta == 0:
            media_idades_reprod.append(calculamedia([a.population[ind].mother_record for ind in range(Constants.population_size)]))
            print 'media_idades'
            fobj = open(base_path+'media_idades.txt', 'w')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
            

        chg = False

    print 'plot'
    fobj = open(base_path+'plot.py', 'w')
    fobj.write('import matplotlib.pyplot as plt\n\nplt.figure()\nplt.plot(')
    fobj.write(str(media_idades_reprod))
    fobj.write(')\n\nplt.show()\nplt.draw()\nplt.draw()')
    fobj.close()
    

def constant_method(env_ind, period, population):
    return (False, 0)

def periodic_method(env_ind, period, population):
    if population.time % Constants.envchg_period == 0:
        return (True, (env_ind + 1)%period)
    return (False, env_ind)

def random_method(env_ind, period, population):
    if rndm.random() < Constants.env_change_rate:
        return (True, rndm.randint(0, period - 1))    
    return (False, env_ind)

def periodic_asymmetric__method(env_ind, period, population):
    if population.time % Constants.envchg_period == 0:
        return (True, (env_ind + 1)%period)
    return (False, env_ind)



if __name__ == '__main__':    

    MetNet = None    

    print ('executing from '+sys.argv[1])
    execution = open(sys.argv[1])

    simulation_n = 0
    while True:
        execution.seek(0)
        for line in execution:
            if line[0] == '#':
                continue
            args = line.split()

            print ('executing simulation '+str(simulation_n), args[0], 'root path is', 
            args[1], 'mutation rate is', Constants.rate)
      
            print 'rate: ' + str(Constants.rate)
        
            base_path = args[1]+str(simulation_n)+'/'
      
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            exec(args[0])
        simulation_n += 1
    
    print '...Done. Ciao!'
  
