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

# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    model.fit(train_x, train_y)
    return model

# lasso Logistic Regression Classifier
def logistic_regression_classifier_lasso(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l1')
    model.fit(train_x, train_y)
    return model

# ridge Logistic Regression Classifier
def logistic_regression_classifier_ridge(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=10)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier RBF
#no more than a couple of 10000 samples
def svm_classifier_rbf(train_x, train_y):

    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model

# SVM Classifier linear
#no more than a couple of 10000 samples
def svm_classifier_linear(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='linear', probability=True)
    model.fit(train_x, train_y)
    return model

# SVM Classifier using cross validation
#no more than a couple of 10000 samples
def svm_cross_validation_rbf(train_x, train_y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in list(best_parameters.items()):
        print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model

# linearSVC Classifier
def svm_classifier_LinearSVC(train_x, train_y):
    from sklearn.svm import LinearSVC
    model = LinearSVC()
    model.fit(train_x, train_y)
    return model


def read_data(dataObj,trainRatio,scale):
    # dataObj = churnprediction.datasets.load_classify_mainActivePre_E1()
    # dataObj = churnprediction.datasets.load_classify_mainActivePre_removeAllZero()
    # Split the dataset with trainRatio
    trainRatio = 0.8

    n_samples = len(dataObj.target)
    sampleBoundary = int(n_samples * trainRatio)

    # Shuffle the whole data
    shuffleIdx = range(n_samples)
    np.random.shuffle(shuffleIdx)

    # Make the training data
    train_x = dataObj.data[shuffleIdx[:sampleBoundary]]
    train_y = dataObj.target[shuffleIdx [:sampleBoundary]]

    # Make the testing data
    test_x = dataObj.data[shuffleIdx[sampleBoundary:]]
    test_y = dataObj.target[shuffleIdx[sampleBoundary:]]

    #Standardization
    if scale:
        scaler = sklearn.preprocessing.StandardScaler().fit(train_x)
        scaler.transform(train_x)
        scaler.transform(test_x)
    # train_y = train.label
    # train_x = train.drop('label', axis=1)
    # test_y = test.label
    # test_x = test.drop('label', axis=1)
    return train_x, train_y, test_x, test_y

def classify(dataObj,test_classifiers,trainRatio=0.8,model_save_file=None,scale=True):
#dataObj is a mat last column is the target
    # test_classifiers = ['NB', 'LR', 'RF', 'DT', 'GBDT']

    model_save = {}
    classifiers = {'NB':naive_bayes_classifier,
                  'KNN':knn_classifier,
                   'LR':logistic_regression_classifier,
                   'LR_lasso':logistic_regression_classifier_lasso,
                   'LR_ridge':logistic_regression_classifier_ridge,
                   'RF':random_forest_classifier,
                   'DT':decision_tree_classifier,
                  'SVM_rbf':svm_classifier_rbf,
                  'SVM_linear':svm_classifier_linear,
                  'SVMCV':svm_cross_validation_rbf,
                  'linearSVC': svm_classifier_LinearSVC,
                  'GBDT':gradient_boosting_classifier
    }
    print('reading training and testing data...')
    train_x, train_y, test_x, test_y = read_data(dataObj,trainRatio,scale)

    for classifier in test_classifiers:
        print('******************* %s ********************' % classifier)
        start_time = time.time()
        model = classifiers[classifier](train_x, train_y)
        train_time = time.time()
        print('training took %fs!' % (train_time - start_time))
        predict = model.predict(test_x)
        print('predict took %fs!' % (time.time() - train_time))
        if model_save_file != None:
            model_save[classifier] = model
        precision = metrics.precision_score(test_y, predict,average='weighted')
        recall = metrics.recall_score(test_y, predict,average='weighted')
        print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        accuracy = metrics.accuracy_score(test_y, predict)
        f1_score = metrics.f1_score(test_y, predict)
        print('accuracy: %.2f%%,f1_score: %.2f%%' % (100 * accuracy,100*f1_score))
        # print('accuracy: %.2f%%' % (100 * accuracy))

    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))

if __name__ == '__main__':
    # data_file = "H:\\Research\\data\\trainCG.csv"
    import churnprediction.datasets
    dataObj  = churnprediction.datasets.load_classify_mainActivePre()
    classify(dataObj,['linearSVC'],model_save_file="/saveModel_all")
