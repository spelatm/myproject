# 这是支持向量机了，我人麻了
# 整个实现就是调包调包调包
# easy code man
# 数学好难

import matplotlib as mpl
## 设置属性防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False


# 1.加载mnist数据集，可以调用sklearn中的load_digits函数，。

from sklearn.datasets import load_digits
digits = load_digits()
image = digits.images
data = digits.data
labels = digits.target

import matplotlib.pyplot as plt


fig = plt.figure(figsize=(6, 6))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)
#绘制数字：每张图像8*8像素点
for i in range(64):
    ax = fig.add_subplot(8, 8, i+1, xticks=[], yticks=[])
    ax.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
    #用目标值标记图像
    ax.text(0, 7, str(digits.target[i]))
plt.show()
# 2.用train_test_split划分数据集
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0)

# 3.比较linear、RBF、poly等核函数的分类性能。
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import time
import numpy as np

svm1 = SVC(C=1, kernel='linear')
svm2 = SVC(C=1, kernel='rbf')
svm3 = SVC(C=1, kernel='poly')
svm4 = SVC(C=1, kernel='sigmoid')

t0 = time.time()
svm1.fit(x_train, y_train)
t1 = time.time()
svm2.fit(x_train, y_train)
t2 = time.time()
svm3.fit(x_train, y_train)
t3 = time.time()
svm4.fit(x_train, y_train)
t4 = time.time()

svm1_score1 = accuracy_score(y_train, svm1.predict(x_train))
svm1_score2 = accuracy_score(y_test, svm1.predict(x_test))

svm2_score1 = accuracy_score(y_train, svm2.predict(x_train))
svm2_score2 = accuracy_score(y_test, svm2.predict(x_test))

svm3_score1 = accuracy_score(y_train, svm3.predict(x_train))
svm3_score2 = accuracy_score(y_test, svm3.predict(x_test))

svm4_score1 = accuracy_score(y_train, svm4.predict(x_train))
svm4_score2 = accuracy_score(y_test, svm4.predict(x_test))

x_tmp = [0, 1, 2, 3]
t_score = [t1 - t0, t2-t1, t3-t2, t4-t3]
y_score1 = [svm1_score1, svm2_score1, svm3_score1, svm4_score1]
y_score2 = [svm1_score2, svm2_score2, svm3_score2, svm4_score2]

plt.figure(facecolor='w', figsize=(12, 6))


plt.subplot(121)
plt.plot(x_tmp, y_score1, 'r-', lw=2, label=u'训练集准确率')
plt.plot(x_tmp, y_score2, 'g-', lw=2, label=u'测试集准确率')
plt.xlim(-0.3, 3.3)
plt.ylim(np.min((np.min(y_score1), np.min(y_score2)))*0.9, np.max((np.max(y_score1), np.max(y_score2)))*1.1)
plt.legend(loc='lower left')
plt.title(u'模型预测准确率', fontsize=13)
plt.xticks(x_tmp, [u'linear-SVM', u'rbf-SVM', u'poly-SVM', u'sigmoid-SVM'], rotation=0)
plt.grid(b=True)

plt.subplot(122)
plt.plot(x_tmp, t_score, 'b-', lw=2, label=u'模型训练时间')
plt.title(u'模型训练耗时', fontsize=13)
plt.xticks(x_tmp, [u'linear-SVM', u'rbf-SVM', u'poly-SVM', u'sigmoid-SVM'], rotation=0)
plt.xlim(-0.3, 3.3)
plt.grid(b=True)

plt.suptitle(u'SVM分类器不同内核函数模型比较', fontsize=16)

plt.show()

# 4.调节RBF核中参数C的范围，查看svm分类器在训练集和测试集的分类准确率变化。
lst = [0.0001, 0.001, 0.01, 0.1, 1, 10]
lst_num = [0, 1, 2, 3, 4, 5]
svm2_score_list1 = []
svm2_score_list2 = []
plt.figure(facecolor='w', figsize=(12, 6))
for i in lst:
    svm2 = SVC(C=i, kernel='rbf')
    svm2.fit(x_train, y_train)
    svm2_score_list1.append( accuracy_score(y_train, svm2.predict(x_train)))
    svm2_score_list2.append( accuracy_score(y_test, svm2.predict(x_test)))


plt.plot(lst, svm2_score_list1, 'r-', lw=2, label=u'训练集准确率')
plt.plot(lst, svm2_score_list2, 'g-', lw=2, label=u'测试集准确率')

plt.legend(loc='lower left')
plt.title(u'模型预测准确率', fontsize=13)
plt.xlim(-0.3, 5)
plt.xticks(lst_num, [u'0.0001', u'0.001', u'0.01', u'0.1', u'1', u'10'], rotation=0)
plt.grid(b=True)
plt.show()
plt.close('all')


# 5.在训练集上用GridSearchCV函数找到rbf核最优的模型参数（C，gamma），并在测试集上测试。


from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]}]

scores = ['precision', 'recall']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(), tuned_parameters, cv=5,
                       scoring='%s_macro' % score)
    clf.fit(x_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred))
    print()


# 6.调用confusion_matrix函数对测试结果做一个简单分析。


from sklearn.metrics import confusion_matrix
table = confusion_matrix(y_test, y_pred, labels=None, sample_weight=None)
accuracy = accuracy_score(y_pred, y_test)
print(table)
print("accuracy:", accuracy)
