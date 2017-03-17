#-*-coding:utf-8-*-
__author__ = 'liuqin212173'
from personas.datasets import *
import personas.datasets

import time
from sklearn import metrics
import pickle as pickle
import pandas as pd
import numpy as np
import personas.datasets
import sklearn.linear_model
import churnprediction.datasets

# chi2_selector
def chi2_selector(train_x, train_y,k=10):
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2
    selection = SelectKBest(chi2,k)
    selection.fit(train_x,train_y)
    # print selection.score_func
    print('----------------------------feature importance -------------------------')
    importance = selection.scores_
    print selection.scores_
    print('----------------------------- selected feature -------------------------')
    print selection.get_support(indices=True)
    return selection,importance


def MINE_selector(train_x, train_y,k=10):
    from sklearn.feature_selection import SelectKBest
    from minepy import MINE

    def mic(x, y):
        m = MINE()
        m.compute_score(x, y)
        return (m.mic(), 0.5)

   #选择K个最好的特征，返回特征选择后的数据
    selection = SelectKBest(lambda X, Y:np.array(map(lambda x:mic(x, Y), X.T)).T, k)
    selection.fit(train_x,train_y)
    selection.scores_ = selection.scores_[0]
    print('----------------------------feature importance -------------------------')
    importance = selection.scores_
    print selection.scores_
    print('----------------------------- selected feature -------------------------')
    print selection.get_support(indices=True)
    return selection,importance



def VarianceThreshold_selector(train_x,train_y,k=10,threshold=0.003):
    from sklearn.feature_selection import VarianceThreshold
    selection = VarianceThreshold(threshold)
    selection = selection.fit(dataObj.data)
    print('----------------------------feature Variance -------------------------')
    # print selection.scores_
    importance = selection.variances_
    print(selection.variances_)
    print('----------------------------- selected feature -------------------------')
    print selection.get_support(indices=True)
    # print(selection.variances_)
    return selection,importance



def RFECV_selector(train_x, train_y,k=10):
    from sklearn.svm import LinearSVC
    from sklearn.feature_selection import RFE
    from sklearn.feature_selection import RFECV
    svc = LinearSVC()
# The "accuracy" scoring is proportional to the number of correct
# classifications
    selection = RFECV(estimator=svc,step=1,
              scoring='accuracy')
    selection.fit(train_x, train_y)
    print('----------------------------feature importance -------------------------')
    print selection.grid_scores_
    importance = selection.grid_scores_
    # print selection.n_features_

    # print(selection.variances_)
    print('----------------------------- selected feature -------------------------')
    print selection.get_support(indices=True)
    return selection,importance


def RFE_selector(train_x, train_y,k=10):
    from sklearn.svm import LinearSVC
    from sklearn.feature_selection import RFE
    from sklearn.feature_selection import RFE
    svc = LinearSVC()
# The "accuracy" scoring is proportional to the number of correct
# classifications
    selection = RFE(estimator=svc,n_features_to_select=k,step=1)

    selection.fit(train_x, train_y)
    # print selection.ranking_
    # print('----------------------------feature importance -------------------------')
    # error
    # print selection.scores_
    importance = None
    # print(selection.variances_)
    print('----------------------------- selected feature -------------------------')
    print selection.get_support(indices=True)

    return selection,importance


def tree_selector(train_x, train_y,k=10):
    from sklearn import tree
    selection = tree.DecisionTreeClassifier(max_features=k)
    selection.fit(train_x, train_y)
    print('----------------------------feature importance -------------------------')
    print selection.feature_importances_
    # print selection.n_features_
    importance = selection.feature_importances_
    # print(selection.variances_)
    # print('----------------------------- selected feature -------------------------')
    # print selection.get_support(indices=True)
    return selection,importance

# Random Forest Classifier
def ExtraTreesClassifier_selector(train_x, train_y,k=10):
    from sklearn.ensemble import ExtraTreesClassifier
    selection = ExtraTreesClassifier(n_estimators=250,max_features=k,
                              random_state=0)

    selection.fit(train_x, train_y)
    print('----------------------------feature importance -------------------------')
    print selection.feature_importances_
    importance = selection.feature_importances_
    #importances = forest.feature_importances_
    return selection,importance



# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_selector(train_x, train_y,k=10):
    from sklearn.ensemble import GradientBoostingClassifier
    selection = GradientBoostingClassifier(n_estimators=200,max_features=k)
    selection.fit(train_x, train_y)
    print('----------------------------feature importance -------------------------')
    print selection.feature_importances_
    importance = selection.feature_importances_
    # print selection.n_features_

    # print(selection.variances_)
    # print('----------------------------- selected feature -------------------------')
    # print selection.get_support(indices=True)
    # return selection

    return selection,importance


def read_data(dataObj,scale):

    train_x = dataObj.data
    train_y = dataObj.target


    #Standardization
    if scale:
        scaler = sklearn.preprocessing.StandardScaler().fit(train_x)
        scaler.transform(train_x)

    # train_y = train.label
    # train_x = train.drop('label', axis=1)
    # test_y = test.label
    # test_x = test.drop('label', axis=1)
    return train_x,train_y

def select(dataObj,test_selectors,k=10,model_save_file=None,scale=True):
#dataObj is a mat last column is the target
    # test_classifiers = ['NB', 'LR', 'RF', 'DT', 'GBDT']

    model_save = {}
    selectors = {'CHI2':chi2_selector,
                  'MINE':MINE_selector,
                   'Variance':VarianceThreshold_selector,
                   'RFECV':RFECV_selector,
                   'RFE':RFE_selector,
                   'DT':tree_selector,
                   'Forest':ExtraTreesClassifier_selector,
                  'GBDT':gradient_boosting_selector
    }
    print('reading training data...')
    train_x, train_y = read_data(dataObj,scale)

    for selector in test_selectors:
        print('******************* %s ********************' % selector)
        start_time = time.time()
        model,importance = selectors[selector](train_x,train_y,k)
        train_time = time.time()
        print('selecting took %fs!' % (train_time - start_time))

        if model_save_file != None:
            model_save[selector] = model


    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))

if __name__ == '__main__':
    # data_file = "H:\\Research\\data\\trainCG.csv"
    import churnprediction.datasets
    dataObj  = churnprediction.datasets.load_classify_mainActivePre()
    dataObj.data = dataObj.data[1:1000,1:12]
    dataObj.target = dataObj.target[1:1000]
    # select(dataObj,['MINE'],model_save_file="../selector_all")
    select(dataObj,['CHI2','GBDT','Variance','RFECV','RFE','DT','Forest'])
