from __future__ import division
import numpy as np
import optunity
#start training process
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
print y
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


#from sklearn.svm import SVC
from sklearn.svm import SVC
import optunity.metrics
# score function: twice iterated 10-fold cross-validated accuracy
@optunity.cross_validated(x=X, y=y, num_folds=10, num_iter=2)
def svm_auc(x_train, y_train, x_test, y_test, logC, logGamma):
    model = SVC(C=10 ** logC, gamma=10 ** logGamma).fit(x_train, y_train)
    decision_values = model.decision_function(x_test)
    return optunity.metrics.roc_auc(y_test, decision_values)

hps, _, _ = optunity.maximize(svm_auc(x_train=X,y_train=y,x_test=test,y_test=t,logC=-5, logGamma=-5), num_evals=200, logC=[-5, 2], logGamma=[-5, 1])

optimal_model = SVC(C=10 ** hps['logC'], gamma=10 ** hps['logGamma']).fit(X, y)

# # clf = SVC()
# clf.fit(X, y)
# SVC(C=1.0, cache_size=200, class_weight='auto', coef0=0.0,
#     decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
#     max_iter=-1, probability=False, random_state=None, shrinking=True,
#     tol=0.001, verbose=False)



result=optimal_model.predict(X)
print result
error=0
for i in range(0,len(result)):
    #print result[i]
    if t[i] !=result[i]:
        error+=1
accuray= (len(result)-error)/len(result)
print "The accuray is: "+str(accuray)+'\n'