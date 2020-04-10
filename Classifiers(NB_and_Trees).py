from tools import *
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import time

def dict_relabel(dicts, label):
    for k in dicts:
        if label in dicts[k][1].split():
            dicts[k][1] = label
        else:
            dicts[k][1] = 'others'
    return dicts

def extract_dataset(dicts, category):
    dataset = {k:v for k, v in dicts.items() if v[0] == category}
    return dataset

def extract_labels(dicts, label):
    y = []
    for k in dicts:
        y.append(dicts[k][1])
    return y

def input_matrix(dicts,label):
    text = []
    features = load_json('json_data/features.json')
    features_label = features[label]
    for k in dicts:
        text.append(dicts[k][2])
    vectorizer = CountVectorizer(vocabulary = features_label)
    dt = vectorizer.fit_transform(text)
    x = dt.toarray()
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i][j] != 0:
                x[i][j] = 1
    return x

def data_prepare(label):
    data = get_dict()
    data1 = dict_relabel(data, label)
    dict_train = extract_dataset(data1, 'TRAIN')
    dict_test = extract_dataset(data1, 'TEST')
    X_train = input_matrix(dict_train, label)
    X_test = input_matrix(dict_test, label)
    y_train = extract_labels(dict_train, label)
    y_test = extract_labels(dict_test, label)
    return X_train, X_test, y_train, y_test

def decision_tree(label, X_train, X_test, y_train, y_test):
    start = time.clock()

    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)

    end = time.clock()
    times.append(end - start)

    y_predict = dtc.predict(X_test)

    # print(label,':', dtc.score(X_test, y_test))
    # print(classification_report(y_test, y_predict, labels=[label, 'others'], target_names=[label, 'others']))
    # p = metrics.precision_score(y_predict, y_test)
    # f1 = metrics.f1_score(y_predict, y_test)
    # return p, f1

def naive_bayes(label, X_train, X_test, y_train, y_test):
    start = time.clock()

    clf = MultinomialNB(alpha=0.0001)
    clf.fit(X_train, y_train)

    end = time.clock()
    times.append(end - start)

    y_predict = clf.predict(X_test)

    # print(classification_report(y_test, y_predict, labels=[label, 'others'], target_names=[label, 'others']))

LABEL = ['acq', 'corn', 'crude', 'earn', 'grain', 'interest', 'money-fx', 'ship', 'trade', 'wheat']
times = []
for i in LABEL:
    X_train, X_test, y_train, y_test = data_prepare(i)
    # decision_tree(i, X_train, X_test, y_train, y_test)
    naive_bayes(i, X_train, X_test, y_train, y_test)
print(np.mean(times))

# dict1 = {}
# for key in y_test:
#     print(dict1.get(key, 0))
#     dict1[key] = dict1.get(key, 0) + 1
# print(dict1)
#
# dict2 = {}
# for key in y_predict:
#     dict2[key] = dict2.get(key, 0) + 1
# print(dict2)
# print(y_test)
# print(y_predict)
# print(len(y_test))
# print(len(y_predict))



# def order_dict(dicts, n):
#     result = []
#     result1 = []
#     p = sorted([(k, v) for k, v in dicts.items()], reverse=True)
#     s = set()
#     for i in p:
#         s.add(i[1])
#     for i in sorted(s, reverse=True)[:n]:
#         for j in p:
#             if j[1] == i:
#                 result.append(j)
#     for r in result:
#         result1.append(r[0])
#     return result1