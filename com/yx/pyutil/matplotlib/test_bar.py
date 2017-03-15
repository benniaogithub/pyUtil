#-*-coding:utf-8-*- 
__author__ = 'liuqin212173'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False
data = np.random.randint(1, 5, [3, 4])
index = np.arange(data.shape[1])
color_index = ['r', 'g', 'b']
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (5, 12))
for i in range(data.shape[0]):
	ax1.bar(index + i*.25 + .1, data[i], width = .25, color = color_index[i],\
	alpha = .5)
for i in range(data.shape[0]):
	ax2.bar(index + .25, data[i], width = .5, color = color_index[i],\
	bottom = np.sum(data[:i], axis = 0), alpha = .7)
ax3.barh(index, data[0], color = 'r', alpha = .5)
ax3.barh(index, -data[1], color = 'b', alpha = .5)
plt.show()
plt.savefig('complex_bar_chart')