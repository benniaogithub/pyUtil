#-*-coding:utf-8-*-
__author__ = 'liuqin212173'
"""
===================================================
Recursive feature elimination with cross-validation
===================================================

A recursive feature elimination example with automatic tuning of the
number of features selected with cross-validation.
"""
print(__doc__)

import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification
import personas.datasets
from sklearn.svm import LinearSVC



# Load the  dataset
dataObj = personas.datasets.load_Discretization()
X = dataObj.data
y = dataObj.target

# Create the RFE object and compute a cross-validated score.
# svc = SVC(kernel="linear")    # large
svc = LinearSVC()
# The "accuracy" scoring is proportional to the number of correct
# classifications
rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(2),
              scoring='accuracy')
rfecv.fit(X, y)

print("Optimal number of features : %d" % rfecv.n_features_)

# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()
