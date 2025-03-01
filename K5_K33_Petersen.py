# Jarosław Grzegorz Socha
import networkx as nx
from src.Utilities import test

test('K5',nx.complete_graph(5))

test('K33',nx.complete_bipartite_graph(3,3))

test('Petersen',nx.petersen_graph())

print("done")