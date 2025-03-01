from src.Dataset import getGraph,allGraphNames
import os
from src.ILP import generateQUBO
from src.Preprocessing import nxCores
import multiprocessing as mp
import pandas as pd
import networkx as nx


threads = 14
pathToCSV = "./data.csv"

# writes None if the graph is planar
def QUBO(file):
    G = getGraph(file)
    C = nxCores(G)

    res = []
    for c in C:
        res.append(generateQUBO(c))
    
    data = open(pathToCSV, "a")
    if res == []:
        data.write(f"{file},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None},{None}\n")
    for i,r in enumerate(res):
        data.write(f"{file},{i},{r[0][0][0]},{r[0][0][1]},{r[0][1][0]},{r[0][1][1]},{r[0][2][0]},{r[0][2][1]},{r[1][0][0]},{r[1][0][1]},{r[1][1][0]},{r[1][1][1]},{r[1][2][0]},{r[1][2][1]},{r[2][0][0]},{r[2][0][1]},{r[2][1][0]},{r[2][1][1]},{r[2][2][0]},{r[2][2][1]}\n")
    data.close()

    print("done",file)


def main():
    threads = 14

    d = allGraphNames()

    df = pd.read_csv(pathToCSV)

    filenames = set(d)-set(df['file'])

    print(len(filenames))

    with mp.Pool(threads) as pool:
        pool.map(QUBO, filenames)
    
    return

main()