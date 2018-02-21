import pydot
import pyparsing
import json
import os
import glob
import networkx as nx
import pygraphviz
from networkx.drawing import nx_agraph

for filename in glob.glob("/home/hongfa/workspace/bzip2_ML/bzip2.ml_cfg/*"):
    print filename
    with open(filename,"r") as f:
        #if nx.Graph(nx.drawing.nx_pydot.read_dot(f)):
        G=nx.Graph(nx.drawing.nx_pydot.read_dot(f))
        #else:continue
#print list(nx.connected_components(G))
    nodes=G.nodes()
    #print nodes
    src=str(sorted(nodes)[0])

    dest=str(sorted(nodes)[-1])

    function_name = filename.split("/home/hongfa/workspace/bzip2_ML/bzip2.ml_cfg/")[1].split(".dot")[0]

    paths = list(nx.all_simple_paths(G,src,dest))
    subfolder = '/home/hongfa/workspace/bzip2_ML/train/' + str(function_name) + '/'
    os.mkdir(subfolder)
    #print function_name
    for i in range(0,len(paths)):
        filename = 'trace_' + str(i)

        with open(subfolder + filename, 'w') as f:
            for j in paths[i]:
                j=int(j,10)
                f.write(format(j, '#04x') + '\n')


        i += 1




