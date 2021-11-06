import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sl

import random

def sigmoid(x):
    return 1.0/(1+np.exp(-x))

alpha = 0.01

def gradDown(train, W, tag):
    for i in range(40):
        t = np.dot(train, W)
        error = tag - sigmoid(t)
        W = W + error*alpha*train.T
    return W


    pass

f = pd.read_csv("testSet.txt", sep='\t', header=None)
print(f)
# f = np.array(f)
# print(f)
# type(f)

print(f[2])

f1 = f[f[2] == 0]
f2 = f[f[2] == 1]

plt.figure()
axes = plt.subplot(1, 1, 1)
label1 = axes.scatter(f1[0], f1[1], s=10, c='red')
label2 = axes.scatter(f2[0], f2[1], s=10, c='blue')
plt.show()
f = f.values
f1 = f1.values
f2 = f2.values

train = f[0:40]
tag_train = f[0:40, 2]
test = f[40:100]
tag_test = f[40:100, 2]
train[:, 2] = 1
test[:, 2] = 1

W = np.random.rand(3, 1)
