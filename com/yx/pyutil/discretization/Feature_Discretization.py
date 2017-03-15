#-*-coding:utf-8-*- 
__author__ = 'liuqin212173'

import numpy as np


#信息增益 进行单变量离散化
class Feature_Discretization(object):

    def __init__(self):

        self.min_interval = 1
        self.min_epos = 0.05
        self.final_bin = []


    def fit(self, x, y, min_interval = 1):
        self.min_interval = min_interval
        x = np.floor(x)
        x = np.int32(x)
        min_val = np.min(x)
        bin_dict = {}
        bin_li = []
        for i in range(len(x)):
            pos = (x[i] - min_val)/min_interval * min_interval  + min_val
            target = y[i]
            bin_dict.setdefault(pos,[0,0])
            if target == 1:
                bin_dict[pos][0] += 1
            else:
                bin_dict[pos][1] += 1

        for key ,val in bin_dict.iteritems():
            t = [key]
            t.extend(val)
            bin_li.append(t)

        bin_li.sort(cmp=None, key=lambda x : x[0], reverse=False)
        print bin_li


        L_index = 0
        R_index = 1
        self.final_bin.append(bin_li[L_index][0])
        while True:
            L = bin_li[L_index]
            R = bin_li[R_index]
            # using infomation gain;
            p1 =  L[1]/ (L[1] + L[2] + 0.0)
            p0 =  L[2]/ (L[1] + L[2] + 0.0)

            if p1 <= 1e-5 or p0 <= 1e-5:
                LGain = 0
            else:
                LGain = -p1*np.log(p1) - p0 * np.log(p0)

            p1 =  R[1]/ (R[1] + R[2] + 0.0)
            p0 =  R[2]/ (R[1] + R[2] + 0.0)
            if p1 <= 1e-5 or p0 <= 1e-5:
                RGain = 0
            else:
                RGain = -p1*np.log(p1) - p0 * np.log(p0)

            p1 = (L[1] + R[1])/ (L[1] + L[2] + R[1] + R[2] + 0.0)
            p0 = (L[2] + R[2])/ (L[1] + L[2] + R[1] + R[2] + 0.0)

            if p1 <= 1e-5 or p0 <= 1e-5:
                ALLGain = 0
            else:
                ALLGain = -p1*np.log(p1) - p0 * np.log(p0)

            if np.absolute(ALLGain - LGain - RGain) <= self.min_epos:
                # concat the interval;
                bin_li[L_index][1] += R[1]
                bin_li[L_index][2] += R[2]
                R_index += 1

            else:
                L_index = R_index
                R_index = L_index + 1
                self.final_bin.append(bin_li[L_index][0])

            if R_index >= len(bin_li):
                break

        print 'feature bin:',self.final_bin


    def transform(self,x):
        res = []
        for e in x:
            index = self.get_Discretization_index(self.final_bin, e)
            res.append(index)

        res = np.asarray(res)
        return res

    def get_Discretization_index(self ,Discretization_vals, val ):
        index = -1
        for i in range(len(Discretization_vals)):
            e = Discretization_vals[i]
            if val <= e:
                index = i
                break

        return index