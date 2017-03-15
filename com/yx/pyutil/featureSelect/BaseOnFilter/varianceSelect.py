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


if __name__ == "__main__":
    dataObj = personas.datasets.load_Discretization()
    # print(np.var(dataObj.data,0))
    from sklearn.feature_selection import VarianceThreshold
    selection = VarianceThreshold(threshold=0.3)
    s = selection.fit(dataObj.data)

    # print(s._get_support_mask())  #[ True False  True  True  True  True  True  True False  True  True  True True  True False False False False False False False False False False]
    print(s.get_params())
    print(s.get_support()) #[ True False  True  True  True  True  True  True False  True  True  True True  True False False False False False False False False False False]
    print(s.variances_)

    #
