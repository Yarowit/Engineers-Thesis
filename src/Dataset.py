# Jarosław Grzegorz Socha
import networkx as nx
import os

pathoToDataset = '/home/jaros/Rome/data'

def getGraph(filename):
    G = nx.read_gml(pathoToDataset+'/'+filename)
    return G

def allGraphNames():
    return os.listdir(pathoToDataset)