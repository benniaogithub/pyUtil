#-*-coding:utf-8-*-
__author__ = 'liuqin212173'
from personas.datasets import *
import personas.datasets
import sklearn.linear_model
import numpy.random
import numpy.linalg
import matplotlib.pyplot
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from os.path import dirname
from os.path import join

def datasetKmeans(data=None):
    if data is None:
        data = personas.datasets.load_mainFunc()

    kmeans = KMeans(n_clusters=5, random_state=0).fit(data)
    print pd.value_counts(kmeans.labels_)
    print(kmeans.cluster_centers_)
    return data,kmeans

def showKmeans3D(data, kmeans, showRatio=0.01):
    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(data)
    n_samples = len(data)
    print("samples:____",n_samples)
    print("showRatio:____",showRatio)

    sampleBoundary = int(n_samples * showRatio)

    # Shuffle the whole data
    shuffleIdx = range(n_samples)
    numpy.random.shuffle(shuffleIdx)

    ax=plt.subplot(111,projection='3d')
    # Make the show data
    # show_features = boston.data[shuffleIdx[:sampleBoundary]]
    show_targets = kmeans.labels_[shuffleIdx [:sampleBoundary]]
    show_pca_result = pca_result[shuffleIdx [:sampleBoundary]]
    # matplotlib.pyplot.plot(range(sampleBoundary), predict_targets[shuffleIdx[:sampleBoundary]], 'r--', label = 'Predict Play time')
    # matplotlib.pyplot.plot(range(sampleBoundary), test_targets[shuffleIdx[:sampleBoundary]], 'g:', label='True Play time')


    # ax.scatter(show_pca_result[show_targets==0,0],show_pca_result[show_targets==0,1],show_pca_result[show_targets==0,2],color='r')
    # ax.scatter(show_pca_result[show_targets==1,0],show_pca_result[show_targets==1,1],show_pca_result[show_targets==1,2],color='g')
    # ax.scatter(show_pca_result[show_targets==2,0],show_pca_result[show_targets==2,1],show_pca_result[show_targets==2,2],color='b')
    # ax.scatter(show_pca_result[show_targets==3,0],show_pca_result[show_targets==3,1],show_pca_result[show_targets==3,2],color='k')
    # ax.scatter(show_pca_result[show_targets==4,0],show_pca_result[show_targets==4,1],show_pca_result[show_targets==4,2],color='brown')

    cm = plt.cm.get_cmap('RdYlBu')
    ax.scatter(show_pca_result[:,0],show_pca_result[:,1],show_pca_result[:,2],c=show_targets*3,cmap=cm,s=5)

    # plt.scatter(show_pca_result[show_targets==5,0],show_pca_result[show_targets==5,1],color='#7FFFD4')
    # legend = matplotlib.pyplot.legend()
    matplotlib.pyplot.title("funcKeans")
    # # matplotlib.pyplot.ylabel("predict play time")
    module_path = dirname(__file__)
    data_file_name = join(module_path, 'pic', 'funcKeans_3D.png')
    matplotlib.pyplot.savefig(data_file_name, format='png')
    # matplotlib.pyplot.show()
    plt.show()

def showKmeans2D(data, kmeans, showRatio=0.01):
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data)
    n_samples = len(data)
    print("samples:____",n_samples)
    print("showRatio:____",showRatio)


    sampleBoundary = int(n_samples * showRatio)

    # Shuffle the whole data
    shuffleIdx = range(n_samples)
    numpy.random.shuffle(shuffleIdx)

    # Make the show data
    # show_features = boston.data[shuffleIdx[:sampleBoundary]]
    show_targets = kmeans.labels_[shuffleIdx [:sampleBoundary]]
    show_pca_result = pca_result[shuffleIdx [:sampleBoundary]]
    # matplotlib.pyplot.plot(range(sampleBoundary), predict_targets[shuffleIdx[:sampleBoundary]], 'r--', label = 'Predict Play time')
    # matplotlib.pyplot.plot(range(sampleBoundary), test_targets[shuffleIdx[:sampleBoundary]], 'g:', label='True Play time')

    cm = plt.cm.get_cmap('RdYlBu')
    plt.scatter(show_pca_result[:,0],show_pca_result[:,1],c=show_targets*3,cmap=cm,s=5)
    # plt.scatter(show_pca_result[show_targets==1,0],show_pca_result[show_targets==1,1],color='g')
    # plt.scatter(show_pca_result[show_targets==2,0],show_pca_result[show_targets==2,1],color='b')
    # plt.scatter(show_pca_result[show_targets==3,0],show_pca_result[show_targets==3,1],color='k')
    # plt.scatter(show_pca_result[show_targets==4,0],show_pca_result[show_targets==4,1],color='brown')
    # plt.scatter(show_pca_result[show_targets==5,0],show_pca_result[show_targets==5,1],color='#7FFFD4')
    # legend = matplotlib.pyplot.legend()
    # matplotlib.pyplot.title("funcKeans")
    # # matplotlib.pyplot.ylabel("predict play time")
    module_path = dirname(__file__)
    data_file_name = join(module_path, 'pic', 'funcKeans_2D.png')
    matplotlib.pyplot.savefig(data_file_name, format='png')

    # matplotlib.pyplot.show()
    plt.show()

if __name__ == "__main__":
    data,kmeans = datasetKmeans()
    showKmeans2D(data,kmeans)