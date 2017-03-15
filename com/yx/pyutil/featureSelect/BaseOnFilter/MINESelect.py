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
    from sklearn.feature_selection import SelectKBest
    from minepy import MINE

    def mic(x, y):
        m = MINE()
        m.compute_score(x, y)
        return (m.mic(), 0.5)

   #选择K个最好的特征，返回特征选择后的数据
    selection = SelectKBest(lambda X, Y:np.array(map(lambda x:mic(x, Y), X.T)).T, k=10)

    selection.fit(dataObj.data, dataObj.target)
    scores = selection.scores_[0]   #这个地方跟其他函数有点异常
    print np.argsort(scores, kind="mergesort")[-10:]

    # mask[np.argsort(scores, kind="mergesort")[-self.k:]] = 1
    # selection._get_support_mask()
    # selection = SelectKBest(chi2, k=10)
    # selection.fit(dataObj.data,dataObj.target)

    # print selection.pvalues_
    # print selection.score_func
    # print selection.scores_

    # print selection.get_support(indices=True)
    #P值不是给定样本结果时原假设为真的概率，而是
    # 给定原假设为真时样本结果出现的概率。
    # print(s._get_support_mask())  #[ True False  True  True  True  True  True  True False  True  True  True True  True False False False False False False False False False False]
    # print(s.get_params())
    # print(s.get_support()) #[ True False  True  True  True  True  True  True False  True  True  True True  True False False False False False False False False False False]
    # print(s.variances_)

    #
