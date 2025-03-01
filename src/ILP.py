# Jarosław Grzegorz Socha
import networkx as nx
import numpy as np
from itertools import combinations
from math import ceil

def properSubsets(s):
    comb = []
    for i in range(1,len(s)):
        comb.extend(set(c) for c in combinations(s, i))
    return comb
    

# NOTE expression squaring
def quadratify(P:nx.Graph, d:list):
    for u,v in combinations(d,2):
        if not P.has_edge(u,v):
            P.add_edge(u,v)

def succ(G,P,x,c,fh):
    V = list(G)
    A = list(G.edges())

    p = {v:{} for v in V}
    for v in V:
        p[v] = {}
        for u in G.neighbors(v):
            p[v][u] = {w:'p.'+str(v)+'.'+str(u)+'.'+str(w) for w in G.neighbors(v) if w != u}

            for w in G.neighbors(v):
                if w != u:
                    P.add_node(p[v][u][w])

    # 7.4 

    for i in range(fh):
        for v in V:
            for u in G.neighbors(v):
                for w in G.neighbors(v):
                    if u == w:
                        continue

                    # e
                    d = []

                    d.append(c[i][(v,w)]) 
                    d.append(c[i][(u,v)]) 
                    d.append(p[v][u][w])

                    # slack
                    name = 'ssucc1.'+str(i)+'.'+str(v)+'.'+str(u)+'.'+str(w)
                    P.add_node(name)
                    d.append(name)

                    quadratify(P,d)

                    # f
                    d = []

                    d.append(c[i][(v,w)]) 
                    d.append(c[i][(u,v)]) 
                    d.append(p[v][u][w])

                    # slack
                    name = 'ssucc2.'+str(i)+'.'+str(v)+'.'+str(u)+'.'+str(w)
                    P.add_node(name)
                    d.append(name)

                    quadratify(P,d)

    # 7.5
    for v in V:
        for u in G.neighbors(v):
            d_g = []
            d_h = []
            for w in G.neighbors(v):
                if u == w:
                    continue
                d_g.append(p[v][u][w])
                d_h.append(p[v][w][u])
            
            quadratify(P,d_g)
            quadratify(P,d_h)

    # 7.6
    for v in V:
        for U in properSubsets(list(G.neighbors(v))):
            d = []
            for u in U:
                for w in set(G.neighbors(v))-U:
                    d.append(p[v][u][w])
            

            inner = min(len(U),len(list(G.neighbors(v)))-len(U))-1
            
            # slack
            r=0
            if inner == 0:
                r = -1
            else:
                r = int(np.log2(inner))

            for t in range(r+1):
                name = 'ssucck.'+str(v)+'.'+str(U)+'.'+str(t)
                P.add_node(name)
                d.append(name)

            quadratify(P,d)

def ind(G,P,x,c,fh):
    V = list(G)
    A = list(G.edges())
    
    q = {v:{} for v in V}
    for v in V:
        q[v] = {}
        for u in G.neighbors(v):
            q[v][u] = {j:'q.'+str(v)+'.'+str(u)+'.'+str(j) for j in range(len(list(G.neighbors(v))))}

            for j in range(len(list(G.neighbors(v)))):
                P.add_node(q[v][u][j])
            

    # 7.7

    for i in range(fh):
        for v in V:
            for j in range(len(list(G.neighbors(v)))):
                for u in G.neighbors(v):
                    for w in G.neighbors(v):
                        if u == w:
                            continue

                        # e
                        d = []

                        d.append(c[i][(v,w)]) 
                        d.append(c[i][(u,v)]) 
                        d.append(q[v][u][j])
                        d.append(q[v][w][(j+1)%len(list(G.neighbors(v)))])

                        # slack
                        name = 'sind1.1.'+str(i)+'.'+str(v)+'.'+str(j)+'.'+str(u)+'.'+str(w)
                        P.add_node(name)
                        d.append(name)

                        name = 'sind1.2.'+str(i)+'.'+str(v)+'.'+str(j)+'.'+str(u)+'.'+str(w)
                        P.add_node(name)
                        d.append(name)

                        quadratify(P,d)

                        # f
                        d = []

                        d.append(c[i][(v,w)]) 
                        d.append(c[i][(u,v)]) 
                        d.append(q[v][u][j])
                        d.append(q[v][w][(j+1)%len(list(G.neighbors(v)))])

                        # slack
                        name = 'sind2.1.'+str(i)+'.'+str(v)+'.'+str(j)+'.'+str(u)+'.'+str(w)
                        P.add_node(name)
                        d.append(name)

                        name = 'sind2.2.'+str(i)+'.'+str(v)+'.'+str(j)+'.'+str(u)+'.'+str(w)
                        P.add_node(name)
                        d.append(name)
                        
                        quadratify(P,d)


    # 7.8 - 1
    for v in V:
        for u in G.neighbors(v):
            d = []
            for j in range(len(list(G.neighbors(v)))):
                d.append(q[v][u][j])

            quadratify(P,d)

    # 7.8 - 2
    for v in V:
        for j in range(len(list(G.neighbors(v)))):
            d = []
            for u in G.neighbors(v):
                d.append(q[v][u][j])

            quadratify(P,d)


def bet(G,P,x,c,fh):
    V = list(G)
    A = list(G.edges())
    
    r = {v:{} for v in V}

    for v in V:
        r[v] = {}
        intNeigh = [int(g) for g in list(G.neighbors(v))]
        for comb in combinations(intNeigh, 3):
            name = str(sorted(comb))
            r[v][name] = 'r.'+str(v)+'.'+name
            P.add_node(r[v][name])

    
    # 7.9

    for i in range(fh):
        for v in V:
            for u in G.neighbors(v):
                for w in G.neighbors(v):
                    if u == w:
                        continue


                    d = []
                    
                    d.append(c[i][(v,w)]) 
                    d.append(c[i][(u,v)]) 
                    for y in G.neighbors(v):
                        if y != u and y != w:
                            d.append(r[v][str(sorted([int(y),int(u),int(w)]))])
                    
                    for k in range(int(np.log2(len(list(G.neighbors(v)))))+1):
                        name = 'sbetone.1.'+str(i)+'.'+str(v)+'.'+str(u)+'.'+str(w)
                        P.add_node(name)
                        d.append(name)

                    quadratify(P,d)

                    # f
                    d = []

                    d.append(c[i][(v,w)]) 
                    d.append(c[i][(u,v)]) 
                    for y in G.neighbors(v):
                        if y != u and y != w:
                            d.append(r[v][str(sorted([int(y),int(u),int(w)]))])
                    
                    for k in range(int(np.log2(len(list(G.neighbors(v)))))+1):
                        name = 'sbetone.2.'+str(i)+'.'+str(v)+'.'+str(u)+'.'+str(w)
                        P.add_node(name)
                        d.append(name)
                    
                    quadratify(P,d)
    
    # 7.10

    for v in V:
        if len(list(G.neighbors(v))) > 3:
            for comb in combinations(list(G.neighbors(v)),4):
                u=comb[0]
                w=comb[1]
                x=comb[2]
                y=comb[3]

                d = []

                d.append(r[v][str(sorted([int(u),int(x),int(y)]))])
                d.append(r[v][str(sorted([int(u),int(w),int(x)]))])
                d.append(r[v][str(sorted([int(u),int(w),int(y)]))])
                name = 'sbettwo.1.1.'+str(v)+'.'+str(sorted([int(u),int(w),int(x),int(y)]))
                P.add_node(name)
                d.append(name)
                name = 'sbettwo.1.2.'+str(v)+'.'+str(sorted([int(u),int(w),int(x),int(y)]))
                P.add_node(name)
                d.append(name)
                quadratify(P,d)

                
                d = []

                d.append(r[v][str(sorted([int(u),int(w),int(x)]))])
                d.append(r[v][str(sorted([int(u),int(x),int(y)]))])
                d.append(r[v][str(sorted([int(w),int(x),int(y)]))])
                name = 'sbettwo.2.1.'+str(v)+'.'+str(sorted([int(u),int(w),int(x),int(y)]))
                P.add_node(name)
                d.append(name)
                name = 'sbettwo.2.2.'+str(v)+'.'+str(sorted([int(u),int(w),int(x),int(y)]))
                P.add_node(name)
                d.append(name)
                quadratify(P,d)
                        

def base(G:nx.Graph):
    E = list(G.edges())
    V = list(G)

    G = G.to_directed()
    A = list(G.edges())
    
    fh = min(2*len(E)//3,len(E)-len(V))

    # they store hashable names of nodes
    x = ['x.'+str(i) for i in range(fh)]
    c = [{a: 'c.'+str(i)+'.'+str(a) for a in A} for i in range(fh)]

    P = nx.Graph()
    P.add_nodes_from(x)
    for i in range(fh):
        for a in A:
            P.add_node(c[i][a])

    # 6.1
    for i in range(fh):
        d = []
        # x
        d.append(x[i])
        # c
        for a in A:
            d.append(c[i][a])
        # slack
        for k in range(int(np.log2(len(A)))+1):
            name = 'sbase1.'+str(i)+'.'+str(k)
            P.add_node(name)

        quadratify(P,d)

    # 6.2
    for a in A:
        d = []
        for i in range(fh):
            d.append(c[i][a])
    
        quadratify(P,d)

    # 6.3
    for i in range(fh):
        for v in V:
            d = []
            for w in G.neighbors(v):
                a_in = (w,v)
                a_out = (v,w)
                d.append(c[i][a_in])
                d.append(c[i][a_out])
            
            quadratify(P,d)


    result = []
    
    T = [6.0,15.0,20.0]

    P1 = P.copy()
    succ(G,P1,x,c,fh)
    
    result.append([(P1.number_of_nodes(),P1.number_of_edges())])
    for tegree in T:
        verts = 0
        for i, deg in P1.degree():
            verts += ceil(deg/tegree)
        result[-1].append((verts, (verts - P1.number_of_nodes())+P1.number_of_edges()))
   
    del P1

    P2 = P.copy()
    ind(G,P2,x,c,fh)
    result.append([(P2.number_of_nodes(),P2.number_of_edges())])
    for tegree in T:
        verts = 0
        for i, deg in P2.degree():
            verts += ceil(deg/tegree)
        result[-1].append((verts, (verts - P2.number_of_nodes())+P2.number_of_edges()))
    
    del P2
    
    
    bet(G,P,x,c,fh)
    result.append([(P.number_of_nodes(),P.number_of_edges())])
    for tegree in T:
        verts = 0
        for i, deg in P.degree():
            verts += ceil(deg/tegree)
        result[-1].append((verts, (verts - P.number_of_nodes())+P.number_of_edges()))
    
    return result


def generateQUBO(G:nx.Graph):
    return base(G)

