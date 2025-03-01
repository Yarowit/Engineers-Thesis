# Jarosław Grzegorz Socha
from src.Dataset import getGraph, allGraphNames

l= []

for i,g in enumerate(allGraphNames()):
    G = getGraph(g)
    l.append(G.number_of_edges()/G.number_of_nodes())

print(sum(l)/len(l))