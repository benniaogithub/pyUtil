#-*-coding:utf-8-*-
__author__ = 'liuqin212173'



from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
import personas.datasets
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel


# Load the  dataset
dataObj = personas.datasets.load_Discretization()
X = dataObj.data
y = dataObj.target

clf = ExtraTreesClassifier()
clf = clf.fit(X, y)
print clf.feature_importances_
model = SelectFromModel(clf, prefit=True)       #选取大于等于默认阈值的特征

print(model.get_support(indices=True))
X_new = model.transform(X)
print X_new.shape

# # Plot pixel ranking
# plt.matshow(ranking, cmap=plt.cm.Blues)
# plt.colorbar()
# plt.title("Ranking of pixels with RFE")
# plt.show()
