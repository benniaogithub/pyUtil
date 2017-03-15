#-*-coding:utf-8-*-
__author__ = 'liuqin212173'

"""
Examples
    --------
    The following example shows how to retrieve the 5 right informative
    features in the Friedman #1 dataset.

    >>> from sklearn.datasets import make_friedman1
    >>> from sklearn.feature_selection import RFE
    >>> from sklearn.svm import SVR
    >>> X, y = make_friedman1(n_samples=50, n_features=10, random_state=0)
    >>> estimator = SVR(kernel="linear")
    >>> selector = RFE(estimator, 5, step=1)
    >>> selector = selector.fit(X, y)
    >>> selector.support_ # doctest: +NORMALIZE_WHITESPACE
    array([ True,  True,  True,  True,  True,
            False, False, False, False, False], dtype=bool)
    >>> selector.ranking_
    array([1, 1, 1, 1, 1, 6, 4, 3, 2, 5])

    References
    ----------

"""

from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
import personas.datasets




# Load the  dataset
dataObj = personas.datasets.load_Discretization()
X = dataObj.data
y = dataObj.target

# Create the RFE object and rank each pixel
svc = SVC(kernel="linear", C=1)

# RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(iris.data, iris.target)
rfe = RFE(estimator=svc, n_features_to_select=1, step=1)       #选一个可以获得所有的特征排序，否则被选的并列第一
rfe.fit(X, y)
ranking = rfe.ranking_
print ranking

# # Plot pixel ranking
# plt.matshow(ranking, cmap=plt.cm.Blues)
# plt.colorbar()
# plt.title("Ranking of pixels with RFE")
# plt.show()
