# Jarosław Grzegorz Socha
import networkx as nx
from src.Utilities import test

for n in range(14):
    test(f'K{n}',nx.complete_graph(n))

for n in range(15):
    G = test(f'K{n}',nx.complete_bipartite_graph(3,n))