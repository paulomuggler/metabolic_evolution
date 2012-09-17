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
from copy import deepcopy

#O ambiente eh gerado antes de mais nada!!!
#Aqui tem que ser decidido sobre as condicoes.



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
            enzime_fraction = peso*float(enzime_fraction)/reac
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
        fobj.write('\ndivision ages:\n' + str([self.population[ind].record for ind in range(pop_size)]))
        fobj.write('\nmothers ages:\n' + str([self.population[ind].mother_record for ind in range(pop_size)]) + '\n\n')
        fobj.close()

        fobj = open(base_path+'species.txt', 'a')
        fobj.write(str([self.population[ind].species for ind in range(pop_size)]) + '\n')
        fobj.close()

    def genometofile(self):
        fobj = open(base_path+'genome.txt', 'a')
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
    if n == 0:
        return 0
    return media/n

def headertofile(string):

    fobj = open(base_path+'header.txt', 'a')
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


def constant_size_environment_random():

    headertofile('constant_size_environment_random')

    global MetNet

    if difficult:
        environ_list = [[True]*(food/3) + [False]*(food - food/3),[False]*(food/3) + [True]*(food/3) + [False]*(food - 2*(food/3)), [False]*(2*(food/3))+ [True]*(food - 2*(food/3))]
    else:
        environ_list = [[True]*food]
        for e in range(number_environments - 1):
            environ_list.append([(1 == rndm.randint(0,1)) for i in range(food)])

    print 'environment!'
    fobj = open(base_path+'environment.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(met, reac, food, targets, difficult or environ_list)
    
    fobj = open(base_path+'MetNet.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 
    a = Population()
    division = []
    env_change_rate = 0.02
    chg = False

    media_idades_reprod = []

    for my_step in xrange(end_step):
        a.step()
        

            
        if rndm.random() < env_change_rate:
            chg = True
            env_ind = rndm.randint(0,len(environ_list) - 1)
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
            fobj = open(base_path+'media_idades.txt', 'w')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        
        chg = False

def constant_size_environment_periodic():

    headertofile('constant_size_environment_periodic')

    global MetNet

    envchg_period = 100

    if difficult:
        environ_list = [[True]*(food/3) + [False]*(food - food/3),[False]*(food/3) + [True]*(food/3) + [False]*(food - 2*(food/3)), [False]*(2*(food/3))+ [True]*(food - 2*(food/3))]
        subenv = 3
    else:
        environ_list = [[True]*(food/2) + [False]*(food - food/2),[False]*(food/2) + [True]*(food - food/2)]
        subenv = 2

    print 'environment!'
    fobj = open(base_path+'environment.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(met, reac, food, targets, difficult or environ_list)

    fobj = open(base_path+'MetNet.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 
    
    a = Population()
    division = []
    chg = False
    env_ind = 0

    media_idades_reprod = []

    for my_step in xrange(end_step):
        a.step()
            
        if a.time%envchg_period == 0:
            chg = True
            env_ind = (env_ind + 1)%subenv
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
            fobj = open(base_path+'media_idades.txt', 'w')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        
        chg = False
            
def constant_size_environment_constant():

    headertofile('constant_size_environment_constant')

    global MetNet

    environ_list = [[True]*food]

    print 'environment!'
    fobj = open(base_path+'environment.txt', 'a')
    fobj.write('environ_list: ' + str(environ_list))
    fobj.close()
        
    MetNet = MetabolicNetwork(difficult or environ_list)

    fobj = open(base_path+'MetNet.txt', 'a')
    fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    fobj.close()
 

    a = Population()
    division = []

    media_idades_reprod = []

    for my_step in xrange(end_step):
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
            fobj = open(base_path+'media_idades.txt', 'w')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
        

if __name__ == '__main__':

  food = 20
  targets = 1
  metabolites = 35
  reactions = 17
  genes = 17
  p = 0.2
  population_size = 100
  division_threshold = 50
  record_size = 10
  rate = 0.0001
  number_environments = 3

  peso = 1.0/3

  ta = 100
  tb = 10000

  MetNet = None

  end_step = 1000000

  print ('executing from '+sys.argv[1])
  execution = open(sys.argv[1])

  simulation_n = 0
  while True:
    execution.seek(0)
    for line in execution:
      args = line.split()

      print ('executing simulation '+str(simulation_n), args[0], 'root path is', 
      args[1], 'mutation rate is', args[2])
      
      rate = float(args[2])
      print 'rate: ' + str(rate)

      difficult = None
      if len(args) > 3:
        difficult = args[3]
        
      base_path = args[1]+str(simulation_n)+'/'
      
      if not os.path.exists(base_path):
        os.makedirs(base_path)
      exec(args[0])
    simulation_n += 1
    
  print '...Done. Ciao!'
  
