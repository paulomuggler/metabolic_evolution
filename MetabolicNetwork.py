#! /usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import time

class TargetException(Exception):
    pass

class FoodException(Exception):
    pass

class MetaboliteNumberException(Exception):
    pass

class MetabolicNetwork(nx.DiGraph):

    #fazer uma versao depois com as reacoes liga/desliga fluindo materia
    #(sem precisar que o path esteja inteiro aberto ao mesmo tempo)
    
    def __init__(self, metabolites, reactions, food, targets, env_list = None):
        nx.DiGraph.__init__(self)
        self.number_metabolites = metabolites
        self.number_reactions = reactions
        self.number_food = food
        self.number_targets = targets
        if targets>metabolites:
            raise TargetException('The number of targets cannot exceed the number of metabolites!')
        if food < 1:
            raise FoodException('There are no food molecules!')
        if targets + food > metabolites:
            raise MetaboliteNumberException('There are more food and target molecules than possible!')


        if env_list is None:
            self.generate_random()
            while not self.is_problem_solvable():
                self.clear()
                self.generate_random()
                

            print 'Solution found!'
            print 'target1:' + str(self.number_food)
            print 'number of targets: ' + str(targets) 
            
            self.target_amount = self.path_to_target() ##Acho que nao ta sendo usado
            self.turn_off_met()

        else:
            self.generate_random()
            flag = False
            while not flag:
                flag = True
                for e in env_list:
                    ver = (self.is_problem_solvable(e) > 0)
                    flag = flag and ver
                if not flag:
                    self.clear()
                    self.generate_random()
            

            print 'Solution multiple environment found!'
            print 'target1:' + str(self.number_food)
            print 'number of targets: ' + str(targets) 
            
            self.target_amount = self.path_to_target() ##Acho que nao ta sendo usado
            self.turn_off_met()
            
            
       
        
    def generate_random(self):
        #gera o digrafo bipartido, com metabolitos e reacoes.
        #pos = {}
        for food in xrange(self.number_food):
            self.add_node(food, {'Type':'M','Food': True ,'Target': False, 'Flowing': True})
        for targ in xrange(self.number_targets):
            self.add_node(targ +self.number_food, {'Type':'M','Food': False ,'Target': True, 'Flowing': False})
        for metab in xrange(self.number_metabolites - self.number_targets - self.number_food):
            #pos[metab] = (0,metab)
            self.add_node(self.number_targets + self.number_food + metab, {'Type':'M','Food': False ,'Target': False, 'Flowing': False})
            
        for react in xrange(self.number_reactions):
            #pos[react+metabolites] = (metabolites, float(react)*metabolites/reactions)
            self.add_node(self.number_metabolites + react,{'Type':'R', 'on': False})
##            inm = rndm.randint(1,3)
            inm = 2
##            outm = rndm.randint(1,3)  #talvez fazer isso ser igual a um...
            outm = 1
            cj = rndm.sample([x for x in self.nodes() if self.node[x]['Type']=='M'],inm+outm)
            for i in range(inm):
                self.add_edge(cj.pop(rndm.randint(0,inm+outm-1-i)), self.number_metabolites + react, {'weight':rndm.randint(1,5)}) #se for precisar desse peso...
            for o in range(outm):
                self.add_edge(self.number_metabolites + react, cj.pop(rndm.randint(0,outm-1-o)),{'weight':rndm.randint(1,5)})

        #print 'reacoes ligadas:'
        #reac_list = [rea for rea in self.node if self.node[rea]['Type'] == 'R']
        #print len([act for act in reac_list if self.node[act]['on'] == True])

    def update_reactions(self, reaction_dict):
        #Faz 'Flowing' virar False pra limpar e comecar de novo, assim como atualiza as reacoes que (des)ligaram.
        #tem que receber um dicionario com as chaves corretas, so com as reacoes a serem atualizadas
    
        for react in reaction_dict:
            self.node[react]['on'] = reaction_dict[react]
        #print 'a lista:'    
        #print [t for t in [rr for rr in self.node if self.node[rr]['Type'] == 'R'] if self.node[t]['on'] == True]
        #print 'o dicionario:'
        #print self.node
        #time.sleep(20)
        for m in [met for met in self.node if self.node[met]['Type'] == 'M']:
            if not self.node[m]['Food']:
                self.node[m]['Flowing'] = False
        return self.path_to_target()

    def update_food(self, food_dict):
        #atualiza estado das food molecules
        
        for f in food_dict:
            self.node[f]['Flowing'] = food_dict[f]

    def path_to_target(self):
        #Tem que sempre ser usado depois de update_reactions, pra ter o 'Flowing' zerado!
        react_list = [x for x in self.nodes() if self.node[x]['Type'] == 'R']
        metab_list = [x for x in self.nodes() if self.node[x]['Type'] == 'M']
        update = True
        react_possible = True
        
        while update:
            update = False
            for r in react_list:
                if self.node[r]['on']:
                    educts = [e for e, x in self.in_edges(r)]
                    for s in range(len(educts)):  
                        react_possible = react_possible and self.node[educts[s]]['Flowing'] 
                    if react_possible:
                        products = self.successors(r)
                        for t in range(len(products)):
                            react_possible = react_possible and self.node[products[t]]['Flowing']
                            self.node[products[t]]['Flowing'] = True
                        if not react_possible:
                            update = True
                    react_possible = True

        #print [x for x in self.node]
        #print 'resultado path_to_target:'
        #print len([x for x in metab_list if (self.node[x]['Target'] == True and self.node[x]['Flowing'] == True)])
        return len([x for x in metab_list if (self.node[x]['Target'] == True and self.node[x]['Flowing'] == True)])

    def is_problem_solvable(self, env = None): #incluir outras configuracoes de comida
        #Esse metodo liga todas as reacoes, tem que usar turn_off_met depois!!!

        for react in [x for x in self.nodes() if self.node[x]['Type'] == 'R']:
            self.node[react]['on'] = True
        #print self.node

        for m in [met for met in self.node if self.node[met]['Type'] == 'M']:
            if not self.node[m]['Food']:
                self.node[m]['Flowing'] = False
        if env != None:
            for f in range(self.number_food):
                self.node[f]['Flowing'] = env[f]
            
        return self.path_to_target()

    def turn_off_met(self): #incluir outras configuracoes de comida
        for react in [x for x in self.nodes() if self.node[x]['Type'] == 'R']:
            self.node[react]['on'] = False
        
        for m in [met for met in self.node if self.node[met]['Type'] == 'M']:
            if self.node[m]['Food']:
                self.node[m]['Flowing'] = True
            else:
                self.node[m]['Flowing'] = False


##MetNet = MetabolicNetwork(50, 80, 20, 3, [[0]*10 + [1]*10, [1]*10 + [0]*10])

