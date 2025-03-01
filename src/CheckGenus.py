# Jarosław Grzegorz Socha
import sage.all as sg
import subprocess

pathToMultigenus = '/home/jaros/multi_genus'

# Converts a graph into multicode format
def GraphIntoMulticode(G:sg.Graph):
    print(list(G))
    
    G.relabel(range(1,G.num_verts()+1))
    file = [G.num_verts()]
    for node in sorted(list(G)):
        for neigh in G.neighbors(node):
            if neigh > node:
                file.append(neigh)
        file.append(0)
        
    file.pop()

    return bytes(file)


# returns the genus of a graph with the multi_genus program
def LibGenus(component:sg.Graph):
    
    core = sg.Graph(component)
    
    multicode = GraphIntoMulticode(core)

    result = subprocess.run(
        [pathToMultigenus],
        input=multicode,
        capture_output=True
    )
    if result.stderr.count(b':') > 1:
        print(result.stderr)
        raise Exception("multiple graphs")
    
    res = result.stderr.splitlines()[0]
    
    res = res.removeprefix(b'graphs with genus ')
    try:
        return int(res[:res.find(b':')])
    except:
        print()

