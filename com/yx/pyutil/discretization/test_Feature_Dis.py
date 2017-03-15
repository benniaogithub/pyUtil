#-*-coding:utf-8-*- 
__author__ = 'liuqin212173'


import numpy as np
import matplotlib.pyplot  as plt
import pandas as pd
import sklearn

if __name__ == "__main__":

   x=[1,1,5,5,5,5,8,8,10,10,10,10,14,14,14,14,15,15,15,15,15,15,18,18,18,18,18,18,18,18,18,20,2,20,20,20,20,20,20,21,21,21,25,25,25,25,25,28,28,30,30,30]
   x=pd.Series(x)
   s=pd.cut(x,bins=[0,10,20,30],labels=[0,1,2])
   print(np.array(s.values))
   d=pd.get_dummies(s)
   print(d)

   #给定阈值，将特征转换为0/1

   binarizer = sklearn.preprocessing.Binarizer(threshold=1.1)
   binarizer.transform(x)

   #类别特征编码 有时候特征是类别型的，而一些算法的输入必须是数值型，此时需要对其编码。
   enc = preprocessing.OneHotEncoder()
   enc.fit([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]])
   enc.transform([[0, 1, 3]]).toarray()  #array([[ 1., 0., 0., 1., 0., 0., 0., 0., 1.]])

   #7.标签编码（Label encoding）
   le = sklearn.preprocessing.LabelEncoder()
   le.fit([1, 2, 2, 6])
   le.transform([1, 1, 2, 6])  #array([0, 0, 1, 2])
   #非数值型转化为数值型
   le.fit(["paris", "paris", "tokyo", "amsterdam"])
   le.transform(["tokyo", "tokyo", "paris"])  #array([2, 2, 1])
