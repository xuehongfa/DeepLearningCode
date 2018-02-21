from __future__ import division
import numpy as np
import optunity
# k nearest neighbours
from sklearn.neighbors import KNeighborsClassifier
# support vector machine classifier
from sklearn.svm import SVC
# Naive Bayes
from sklearn.naive_bayes import GaussianNB
# Random Forest
from sklearn.ensemble import RandomForestClassifier
import optunity.metrics
X=[]
test=[]
with open("/home/hongfa/Dropbox/BinaryCode-Hunter/BinaryCode/train-file.vec.txt", "r") as f:
    vec = f.readlines()
vec = [x.strip() for x in vec]
for v in vec:
    v_np=np.fromstring(v, dtype=float,sep=' ')
    temp=np.array(v_np)
    v_final = list(temp)
    X.append(v_final)

X=np.array(X)
print "Training data size is:"+ str(len(X))+'\n'
with open("/home/hongfa/Dropbox/BinaryCode-Hunter/BinaryCode/bzip2_lable.txt", "r") as f:
    lable = f.readline()
#lable = [x.strip() for x in lable]

#v=v.replace(" ",", ")
y=np.fromstring(lable, dtype=int,sep=' ')
y = np.array(y)
#print y
#start testing process
with open("/home/hongfa/Dropbox/BinaryCode-Hunter/BinaryCode/test-file.vec.txt", "r") as f:
    vec = f.readlines()
vec = [x.strip() for x in vec]
for v in vec:
    # v=v.replace(" ",", ")
    v_np = np.fromstring(v, dtype=float, sep=' ')
    # v=np.array(np.array(list(v), dtype=float))
    temp = np.array(v_np)
    # print temp.shape
    v_final = list(temp)
    # print v_final
    test.append(v_final)
test=np.array(test)
print "Testing data size is:"+ str(len(test))+'\n'

with open("/home/hongfa/Dropbox/BinaryCode-Hunter/BinaryCode/bzip2_test_lable.txt", "r") as f:
    test_lable = f.readline()

t=np.fromstring(test_lable, dtype=int,sep=' ')
t = np.array(t)

print y
from sklearn.model_selection import train_test_split
train, test, train_labels, test_labels = train_test_split(X,
                                                          y,
                                                          test_size=0.33,
                                                          random_state=42)
gnb = GaussianNB()
model = gnb.fit(train, train_labels)
preds = gnb.predict(test)
print(preds)

from sklearn.metrics import accuracy_score
print(accuracy_score(test_labels, preds))
