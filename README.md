***Algorithms for the minimum genus of a graph***
*Jarosław Grzegorz Socha*

The thesis explores usage of quantum annealing for theminimum genus of a graph problem (see Thesis.pdf)

The experiments were conducted on a graph dataset 'Rome'

The files contained in this folder consist of all the programs used for the thesis.

***Necessary prerequisites***
* python3
* networkx package
* [sage](https://www.sagemath.org) package

***Programs***

**K5_K33_Petersen.py**
Returns the number of vertices and edges of a model and on diffrent topologies, in a format:
*graph, model, topology degree, vertices, edges*

**Note**
To prepare for launching the following programs connected to dataset, download the dataset in *gml* format, and then set *pathoToDataset* variable in *Dataset* file to the path to the dataset.

**AvaregeDegree.py**
Returns the average degree of the graphs in the dataset.

**Kn_K3n.py**
Does the same thing as K5_K33_Petersen.py, but with graphs *Kn* and *K3n* for given ranges of n.

**ProcessDataset.py**
Calculates the number of vertices and edges for each model and each topology, and puts them in a *.csv* file. The program uses threads and saves data, so it can be stopped and resumed at any time, for batch processing.

To use it, fill the *threads* variable with number of desired threads and *pathToCSV* with the path to the *.csv* file, for which a template can be seen in *res/data.csv*. The already gathered info is in *dataFilled.csv*.

In the table, first letter of a column indicates topology, the string after *_* represents the model, and the next one either edges or vertices.