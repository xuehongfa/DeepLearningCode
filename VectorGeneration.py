import glob
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
#import matplotlib.pyplot as plt
from itertools import cycle
import numpy

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

N = []
V = []
for filename in glob.glob("/home/hongfa/workspace/NorCodeRegion/bzip2_50_1/*.txt"):
    with open(filename) as f:
        Nor_inst = f.readlines()

        for i in Nor_inst:
            i = i.split("\n")[0]
            if i not in N:
                N.append(i)


print len(N)
#n = 0
#print N
Num_node = 0
Data = []
clusters = []
#F = open("/Users/Ben/Downloads/Deckard-parallel1.3/scripts/clonedetect/vectors/vdb_50_1", "a")
for filename in glob.glob("/home/hongfa/workspace/NorCodeRegion/bzip2_50_1/*.txt"):
    #print filename
    for n in range(len(N)):
        V.append(0)

    Vector_filename = filename.split(".")[0].split("bzip2_50_1/")[1].split(".txt")[0]


    line = Vector_filename.split("_")[-2]
    offset = Vector_filename.split("_")[-1]
    with open(filename) as f:
        Nor_inst = f.readlines()

        for i in Nor_inst:
            i = i.split("\n")[0]
            idx = N.index(i)
            V[idx] = V[idx] + 1
            Num_node = Num_node +1

    clone = Vector_filename+","+ "LINE:"+line+", OFFSET:"+offset
    #if Num_node >= 30:    #F = open("/Users/Ben/Documents/BinaryClone/Vectors/"+Vector_filename, "w")
    #F.write("#"+ Vector_filename+", LINE:"+line+", OFFSET:"+offset+", NODE_KIND:65, CONTEXT_KIND:0, NEIGHBOR_KIND:0, NUM_NODE:"+str(Num_node)+", NUM_DECL:0, NUM_STMT:0, NUM_EXPR:0, TBID:"+line+", TEID:"+offset+", VARs:{}15,"+"\n"+" ".join(str(elem) for elem in V)+"\n")
    clusters.append(clone)
    Data.append(V)
    #print V

    Num_node = 0
    V = []
print len(Data)
#print len(Lable)
data = scale(Data)
#print len(data)
#X = PCA(n_components=2).fit_transform(data)
X = data
#print len(X)
af = AffinityPropagation(preference=-50).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Number of clusters: %d' % n_clusters_)

#plt.close('all')
#plt.figure(1)
#plt.clf()
check=0
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    #Total_exact = Total_exact + len(X[cluster_centers_indices[k]])
    F1 = open("./clusters/cluster_"+str(k),"a")
    F2= open("./clusters/Exact_"+str(k),"a")
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    #F2.write(str(len(X[cluster_centers_indices[k]]))+"\n")




    #print Total_exact

    #plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    #plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             #markeredgecolor='k', markersize=14)
    for x in X[class_members]:

        index = 0
        for i in data:

            #print i
            #print x
            if (i == x).all():
                F1.write(clusters[index] + "\n")
                dist = numpy.linalg.norm(x - X[cluster_centers_indices[k]])
                if (dist == 0.0):
                    check = check + 1
                    F2.write(clusters[index] + "\n")
                #print index

            else:
                index = index+1


        #plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

        #idx = X.index[x]:q

        #F.write(Lable[idx]+"\n")
print check
#plt.title('Estimated number of clusters: %d' % n_clusters_)
#plt.show()