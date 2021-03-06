#-*-coding:utf-8-*- 
__author__ = 'liuqin212173'
import personas.util.kmeansUtil as ku
import personas.datasets
from os.path import dirname
from os.path import join
import os
from personas.util import *
from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus



def createDataSet():
    module_path = dirname(__file__)
    data_file_name = join(module_path, 'data', 'funcKmeansLables.npy')
    #np.save("saved_b.npy",b) c=np.load("saved_b.npy")
    dataObj = personas.datasets.load_Discretization()
    if os.path.exists(data_file_name):
        lables = load(data_file_name)
        return dataObj.data,lables
    data,kmeans = datasetKmeans()
    lables = kmeans.labels_
    return dataObj.data,lables

if __name__ == '__main__':
    data,target = createDataSet()
    clf = tree.DecisionTreeClassifier()
    #clf.feature_importances_
    clf = clf.fit(data,target)




    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("funcKmeans.pdf")
