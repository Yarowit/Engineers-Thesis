# Jarosław Grzegorz Socha
import sage.all as sg
from itertools import combinations
from sage.graphs.connectivity import blocks_and_cut_vertices
import networkx as nx

def BiconnectedComponents(G:sg.Graph):       
    blocks, verts = blocks_and_cut_vertices(G)
    components = []
    for block in blocks:
        component = sg.Graph()
        for edge in combinations(block,2):
            if G.has_edge(edge):
                component.add_edge(edge)
        components.append(component)
    return components

def edges(g:sg.Graph):
    e = []
    for u,v in combinations(g,2):
        if g.has_edge(u,v):
            for label in g.edge_label(u,v):
                e.append((u,v,label))
    return e

def Planar(G:sg.Graph):
    if G.num_verts() <= 4:
        return True
    elif G.num_edges() > 3*G.num_verts()-6 or not G.is_planar():
        return False
    else:
        return True
    
def spqr(G:sg.Graph):
    T = sg.Graph.spqr_tree(G)
    
    subs = list(T)

    labels = {}
    i = 0
    for v in T:
        labels[v] = i
        i+=1

    T.relabel(labels)
    for i in range(T.num_verts()):
        T.set_vertex(i,subs[i])
        
    return T



def nonPlanarCore(G:sg.Graph):
    T = spqr(G)

    candidates = [node for node in T if T.degree(node) == 1]

    # remove all planar leafs
    # NOTE removenig means making an unreal edge into a real one
    while len(candidates) > 0:
        leaf = candidates.pop()
        t, subgraph = T.get_vertex(leaf)

        if t != 'R' or subgraph.is_planar():
            parent = T.neighbors(leaf)[0]
            parent_t, parent_graph = T.get_vertex(parent)

            virtual_edge = [edge for edge in edges(subgraph) if edge[2]!=None][0]

            # NOTE real-ify
            changed = sg.Graph(multiedges=True)

            other_edges = [(u,v,label) if ((u,v,label) != virtual_edge and (v,u,label) != virtual_edge) else (u,v,None) for (u,v,label) in edges(parent_graph)]
            
            changed.add_edges(other_edges)
            
            T.set_vertex(parent,(parent_t,changed))

            T.delete_vertex(leaf)
            
            if T.degree(parent) == 1:
                candidates.append(parent)


    # return a graph of only real (None) edges
    
    C = sg.Graph()
    for node in T:
        subgraph = T.get_vertex(node)[1]
        real_edges = [(u,v,label) for (u,v,label) in edges(subgraph) if label == None]

        C.add_edges(real_edges)
    
    # contract edges of degree 2
    for_contraction = [i for i in C if C.degree(i) == 2]
    for i in for_contraction:
        C.merge_vertices([C.neighbors(i)[0],i])
    
    C.relabel(range(C.num_verts()))

    return C


def nxCores(G:nx.Graph):
    C = BiconnectedComponents(sg.Graph(G))
    cores = []

    for component in C:
        if not Planar(component):
            core = nonPlanarCore(component)
            cores.append(core.networkx_graph())

    return cores