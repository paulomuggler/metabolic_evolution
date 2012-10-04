import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from MetabolicNetwork import MetabolicNetwork
from Control import Control
from Constants import Constants
from copy import deepcopy


food = Constants.food
met = Constants.metabolites
reac = Constants.reactions
interm = Constants.intermediate
listadenos = []

#Colocar o DNA do individuo

D = [0, 0, 1.0, 1, -1, -1, 0, 1, 1, -1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, -1, -1, 0, 1, 1, 0, 1, 0, 0, 1, -1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, -1, -1, -1, 0, 1, 1, 0, 0, -1, -1, 0, 0, 0, -1, 1, -1, 0, -1, 0, 1, -1, -1, 1, -1, 0, 0, -1, -1, -1, 1, 0, 1, 0, 0, -1, 1, 0, -1, -1, 1, 1, 0, -1, -1, 1, 0, 1, -1, -1, -1, 1, 0, 1, 1, 0, 0, -1, 1, -1, -1, 1, -1, -1, 1, 1, 0, -1, -1, -1, 1, 1, -1, 0, 0, 0, -1, -1, -1, -1, 1, 1, 1, 1, -1, 0, -1, 1, 0, 0, -1, 0, -1, -1, 0, -1, 0]

pot_cn = (food + reac + interm)
K = food*pot_cn
       
for index in (i for i in xrange(len(D)) if abs(D[i]) == 1):
    a = (index + K)%pot_cn
    b = (index + K - a)/pot_cn
    aa = a if a in range(food) else a + met - food
    bb = b + met - food
    if aa not in listadenos:
        listadenos.append(aa)
    if bb not in listadenos:
        listadenos.append(bb)

listadenos.sort()

def draw_BN(graph, positions, listadenos):
    plt.clf()
    nx.draw_networkx_labels(graph, positions)
    nx.draw_networkx_nodes(graph,positions, nodelist = listadenos, node_color=graph.colors,node_size=150)
    nx.draw_networkx_edges(graph,positions,alpha=0.3)
    plt.draw()

#completar com os estados

on = [True, True, False, True, True, True, False, False, True, False, False, False, False]

fl = [on[j] for j in range(food)]
env_list = [[True, True], [False, True], [True, True], [True, False], [True, True], [False, False]]
period = len(env_list)

index = (env_list.index(fl) + 1)%period


mae = nx.Graph()

for i in range(len(listadenos)):
    mae.add_node(listadenos[i], {'on': on[i]})

control = Control(DNA = D, mother = mae)

for i in range(50):
    draw_BN(control, control.pos, control.genes_list)
    control.change_state()
    time.sleep(1)
    if i%5 == 4:
        control.change_environment(env_list[index])
        index = (index+1)%period

