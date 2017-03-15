#-*-coding:utf-8-*-
__author__ = 'liuqin212173'



from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
import personas.datasets
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.feature_selection import SelectFromModel
import logging
import logging.config
from sklearn import cross_validation

logging.config.fileConfig("E:/python/teemo/log/logger.conf")
logger = logging.getLogger("file")

# Load the  dataset
dataObj = personas.datasets.load_Discretization()
X = dataObj.data
y = dataObj.target

lsvc = LinearSVC(C=0.0005, penalty="l1", dual=False).fit(X, y)    #the smaller C the fewer features selected. With Lasso,
                                                                 #  the higher the alpha parameter, the fewer features selected.
print lsvc.score(X, y)
model = SelectFromModel(lsvc, prefit=True,threshold=0.01)       #选取大于等于默认阈值的特征
logger.info(model.get_support(indices=True))
print(model.get_support(indices=True))
X_new = model.transform(X)
clf = SVC(kernel='linear', C=1)
scores = cross_validation.cross_val_score(clf, X_new,y, cv=5)
# lsvc = LinearSVC(C=0.0001, penalty="l1", dual=False).fit(X_new, y)
print scores
logger.info(X_new.shape)

print X_new.shape

# # Plot pixel ranking
# plt.matshow(ranking, cmap=plt.cm.Blues)
# plt.colorbar()
# plt.title("Ranking of pixels with RFE")
# plt.show()
