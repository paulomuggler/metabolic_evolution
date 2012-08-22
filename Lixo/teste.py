
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import time

G=nx.barabasi_albert_graph(100,3)

grey = "#C0C0C0"
red ="#FF0000"
green="#00FF00"
blue="#0000FF"
cyan="#00FFFF"
magenta="#FF00FF"
yellow="#FFFF00"
white="#FFFFFF"

palette = []
palette.append(grey)
palette.append(red)
palette.append(green)
palette.append(blue)
palette.append(cyan)
palette.append(magenta)
palette.append(yellow)
palette.append(white)

colors = []

w,h=plt.figaspect(1)
plt.figure(figsize=(w,h))

plt.ion()
for n in G.nodes():
   for j in range(3):
       G.node[n][j]=numpy.random.random_integers(0,1)

   c = 1 * G.node[n][0] + 2 * G.node[n][1] + 4 * G.node[n][2]
   colors.append(palette[c])

pos=nx.circular_layout(G)
nodes=nx.draw_networkx_nodes(G,pos,node_color=colors,node_size=50)
edges=nx.draw_networkx_edges(G,pos,alpha=0.3)
plt.draw()

for n in range(100):
   for j in range(3):
       G.node[n][j]=numpy.random.random_integers(0,1)
   c = 1 * G.node[n][0] + 2 * G.node[n][1] + 4 * G.node[n][2]
   colors[n]=palette[c]
   plt.clf()
   nx.draw_networkx_nodes(G,pos,node_color=colors,node_size=50)
   nx.draw_networkx_edges(G,pos,alpha=0.3)
   plt.draw()
   #time.sleep(0.1)
