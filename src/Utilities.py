# Jarosław Grzegorz Socha
from src.ILP import generateQUBO
import networkx as nx

models = ['succ','ind','bet']
T = ['any',6.0,15.0,20.0]

def test(name,G:nx.Graph):
    res = generateQUBO(G)
    for i,model in enumerate(res):
        for j,top in enumerate(model):
            print(name,models[i],T[j],top[0],top[1])
