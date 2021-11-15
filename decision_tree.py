# 歇逼了
# 决策树算法
import pandas as pd
from math import log
import operator
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def loadData():
    data = []
    f = open('lenses.txt')
    for line in f.readlines():
        line_data = line.strip().split('\t')
        data.append(line_data)
    labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    return data, labels

def calshannonent(data):
    nument = len(data)
    labelcounts = {}
    for feat in data:
        currentlabel = feat[-1]
        if currentlabel not in labelcounts.keys():
            labelcounts[currentlabel] = 0
        labelcounts[currentlabel] += 1

    shannonent = 0.0
    for keys in labelcounts:
        prob = float(labelcounts[keys])/nument
        shannonent -= prob * log(prob, 2)

    return shannonent

def calgini(data):
    nument = len(data)
    labelcounts = {}
    for feat in data:
        currentlabel = feat[-1]
        if currentlabel not in labelcounts.keys():
            labelcounts[currentlabel] = 0
        labelcounts[currentlabel] += 1

    gini = 0.0
    for keys in labelcounts:
        prob = float(labelcounts[keys])/nument
        gini += 1 - prob ** 2

    return gini


# def createdata():
#     dataset = [[1, 1, 'yes'],
#                [1, 1, 'yes'],
#                [1, 0, 'no'],
#                [0, 1, 'no'],
#                [0, 1, 'no']]
#     labels = ['no surfacing', 'flippers']
#     return dataset, labels

def splitdata(data, axis, value):
    retdata = []
    for feat in data:
        if feat[axis] == value:
            reducedfeat = feat[:axis]
            reducedfeat.extend(feat[axis+1:])
            retdata.append(reducedfeat)
    return retdata

def choosebestfeaturetosplit(data):
    numfeatures = len(data[0]) - 1
    baseEntropy = calshannonent(data)
    bestinfogain = 0.0
    bestfeatures = -1
    for i in range(numfeatures):
        featlist = [example[i] for example in data]
        uniquevals = set(featlist)
        newEntropy = 0.0
        for value in uniquevals:
            subDataset = splitdata(data, i, value)
            prob = len(subDataset) / float(len(data))
            newEntropy += prob * calshannonent(subDataset)
        infogain = baseEntropy - newEntropy
        if infogain > bestinfogain:
            bestinfogain = infogain
            bestfeatures = i
    return bestfeatures

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClasCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClasCount[0][0]

def createTree(data, labels):
    classList = [example[-1] for example in data]
    if classList.count(classList[0] == len(classList)):
        return classList[0]
    if len(data[0]) == 1:
        return majorityCnt(classList)
    if len(labels) == 0:
        return
    bestFeat = choosebestfeaturetosplit(data)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in data]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitdata(data, bestFeat, value), subLabels)

    return myTree

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

# def createPlot():
#     fig = plt.figure(1, facecolor='white')
#     fig.clf()
#     createPlot.ax1 = plt.subplot(111, frameon=False)
#     plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#     plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#     plt.show()

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[0])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    numleafs = getNumleafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.x0ff + (1.0 + float(numleafs))/2.0/plotTree.totalW,
               plotTree.y0ff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.y0ff = plotTree.y0ff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ =='dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.x0ff = plotTree.x0ff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.x0ff, plotTree.y0ff),
                     cntrPt, leafNode)
            plotMidText((plotTree.x0ff, plotTree.y0ff), cntrPt, str(key))
    plotTree.y0ff = plotTree.y0ff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumleafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.x0ff = -0.5/plotTree.totalW
    plotTree.y0ff = 1.0
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

def getNumleafs(myTree):
    numleafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numleafs += getNumleafs(secondDict[key])
        else:
            numleafs +=1
    return numleafs


def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1+getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listoftree = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]

    return listoftree[i]

if __name__ == '__main__':
    data, labels = loadData()
    shannonent = calshannonent(data)
    gini = calgini(data)
    print("该数据集的信息熵为:", shannonent,
          "该数据集的基尼系数为:", gini)
    k = createTree(data, labels)
    createPlot(k)
