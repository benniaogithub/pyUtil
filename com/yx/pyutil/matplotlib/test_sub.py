#-*-coding:utf-8-*-
__author__ = 'liuqin212173'

import numpy as np
import matplotlib.pyplot  as plt

if __name__ == "__main__":

    # boston = personas.datasets.load_raw_mainActivePre()

    plt.figure(1)#创建图表1
    plt.figure(2)#创建图表2
    ax1=plt.subplot(211)#在图表2中创建子图1
    ax2=plt.subplot(212)#在图表2中创建子图2
    x=np.linspace(0,3,100)
    for i in xrange(5):
        plt.figure(1)
        plt.plot(x,np.exp(i*x/3))
        plt.sca(ax1)
        plt.plot(x,np.sin(i*x))
        plt.sca(ax2)
        plt.plot(x,np.cos(i*x))

    plt.show()


    # #概率分布直方图
    # #高斯分布
    # #均值为0
    # mean = 0
    # #标准差为1，反应数据集中还是分散的值
    # sigma = 1
    # x=mean+sigma*np.random.randn(10000)
    # fig,(ax0,ax1) = plt.subplots(nrows=2,figsize=(9,6))
    # #第二个参数是柱子宽一些还是窄一些，越大越窄越密
    # ax0.hist(x,40,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)
    # ##pdf概率分布图，一万个数落在某个区间内的数有多少个
    # ax0.set_title('pdf')
    # ax1.hist(x,20,normed=1,histtype='bar',facecolor='pink',alpha=0.75,cumulative=True,rwidth=0.8)
    # #cdf累计概率函数，cumulative累计。比如需要统计小于5的数的概率
    # ax1.set_title("cdf")
    # fig.subplots_adjust(hspace=0.4)
    # plt.show()

    # fig,((ax0,ax1,ax2),(ax3,ax4,ax5),(ax6,ax7,ax8)) = plt.subplots(nrows=3,ncols=3,figsize=(20,16))
    # print()
    # ax0.hist(boston.data[:,13],bins=100,normed=True,range=(0,20000))
    # ax0.set_title('step')
    # ax1.hist(boston.data[:,8],bins=100,normed=True,range=(0,80))
    # ax1.set_title('last5s')  #一起涨知识收听时长
    # ax2.hist(boston.data[:,7],normed=True)
    # ax2.set_title('b7peidai')
    # ax3.hist(boston.data[:,0],normed=True)
    # ax3.set_title('age')
    # ax4.hist(boston.data[:,5],normed=True)
    # ax4.set_title('b7sendca11')
    # ax5.hist(boston.data[:,4],normed=True)
    # ax5.set_title('b7zaobao')
    # ax6.hist(boston.data[:,3],normed=True)
    # ax6.set_title('b7zaixian')
    # ax7.hist(boston.data[:,2],normed=True)
    # ax7.set_title('city1eve1')
    # ax8.hist(boston.data[:,1])
    # ax8.set_title('gender')
    #
    #
    #
    #
    #
    #
    # plt.show()