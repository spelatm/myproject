import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sl
import random

# alpha = 0.001
# def sigmoid(x):
#     return 1.0/(1+np.exp(-x))
#
# def gradDown(train, W, tag):
#     for i in range(500):
#         t = np.dot(W, train.T)
#         error = tag - sigmoid(t)
#         W = W + alpha*np.dot(error, train)
#     return W
# def plot(W):
#     n = np.shape(f)[0]
#     xcord1 = []
#     ycord1 = []
#     xcord2 = []
#     ycord2 = []
#     for i in range(n):
#         if int(f[i, 2]) == 1:
#             xcord1.append(f[i, 0])
#             ycord1.append(f[i, 1])
#         else:
#             xcord2.append(f[i, 0])
#             ycord2.append(f[i, 1])
#     fig1 = plt.figure()
#     ax = fig1.add_subplot(111)
#     ax.scatter(xcord1, ycord1, s =10, c='red',marker='s')
#     ax.scatter(xcord2, ycord2, s=10, c='blue')
#     x = np.arange(-3.0, 3.0, 0.1)
#     y = (-W[2]-W[0]*x)/W[1]
#     ax.plot(x, y)
#     plt.xlabel('X1')
#     plt.ylabel('X2')
#     plt.show()
#
# f = pd.read_csv("testSet.txt", sep='\t', header=None)
# #print(f)
# # f = np.array(f)
# # print(f)
# # type(f)
#
# print(f[2])
#
# f1 = f[f[2] == 0]
# f2 = f[f[2] == 1]
#
# # plt.figure()
# # axes = plt.subplot(1, 1, 1)
# # label1 = axes.scatter(f1[0], f1[1], s=10, c='red')
# # label2 = axes.scatter(f2[0], f2[1], s=10, c='blue')
# # plt.show()
# f = f.values
# f1 = f1.values
# f2 = f2.values
#
# train_wait = f[0:100]
# train = np.array(train_wait,copy=True)
# tag_train = np.array(f[0:100, 2], copy=True)
# test_wait = f[40:100]
# test = np.array(test_wait,copy=True)
# tag_test = np.array(f[40:100, 2], copy=True)
# train[:, 2] = 1
# test[:, 2] = 1
#
# W = np.random.rand(1, 3)
# gradDown(train, W, tag_train)
# print(W)
# plot(W.T)




def loadDataset():
    datamat = []
    labelmat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        linearr = line.strip().split()
        ll = [float(linearr[0]), float(linearr[1]), 1]
        datamat.append(ll)
        labelmat.append(int(linearr[2]))
    return datamat, labelmat

def sigmoid(X):
    return 1.0/(1+np.exp(X))

def grandascent(datamatin, classlabels,alpha,maxtrix):
    datamatrix = np.mat(datamatin)
    labelmat = np.mat(classlabels).transpose()
    m, n = np.shape(datamatrix)
    print(m, n)
    # alpha = 0.001
    # maxcycles = 500
    weight = np.ones((n, 1))
    for k in range(maxcycles):
        h = sigmoid(datamatrix*weight)
        error = (labelmat - h)
        weight = weight - alpha * datamatrix.transpose() * error
    return weight

def plot(W):
    datamat, labelmat = loadDataset()
    dataArr = np.array(datamat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelmat[i]) == 1:
            xcord1.append(dataArr[i, 0])
            ycord1.append(dataArr[i, 1])
        else:
            xcord2.append(dataArr[i, 0])
            ycord2.append(dataArr[i, 1])
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.scatter(xcord1, ycord1, s =10, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=10, c='blue')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (- W[2] - W[0] * x) / W[1]
    ax.plot(x, y.T)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

if __name__ == '__main__':
   dataArr, labelMat = loadDataset()
   alpha = 0.001
   maxcycles = 500
   # alpha = float(eval(input("请输入学习率:")))
   # maxcycles = int(eval(input("请输入最大迭代次数：")))
   weight = grandascent(dataArr, labelMat, alpha, maxcycles)
   print(weight)
   plot(weight)