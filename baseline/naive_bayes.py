import os
import sys
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()



path = os.getcwd() + "/big/"
train_path = os.getcwd() + "/big_train/"
test_path = os.getcwd() + "/big_test/"


# path = os.getcwd() + "/dataset/"
# train_path = os.getcwd() + "/text2time_train/"
# test_path = os.getcwd() + "/text2time_test/"


meta_dict = Counter()

train_data = []
train_target = []
test_data = []
test_target = []

def classifyDecade():
    print('createMetaDict()')
    inf = open(path + "meta.csv", encoding='mac_roman')
    lines = inf.readlines()

    # id -> [YYYY, MM, CATEGORY]
    for i in range(len(lines)):
        target = lines[i].replace(',','')
        target = target.rstrip('\n').split()
        meta_dict[target[0]] = target[1:]


    num_train = 0
    for f in os.listdir(train_path):
        if 'csv' in f:
            continue
        if 'zip' in f:
            continue
        filename = f.split('.')[0]
        year = int(meta_dict[filename][0])
        decade_class = (year % 1960) // 10
        if year < 1960:
            continue
        inf = open(train_path + f, "r", encoding='mac_roman')
        art = inf.read()
        train_data.append(art)
        train_target.append(decade_class)
        num_train += 1

    num_test = 0
    for f in os.listdir(test_path):
        if 'csv' in f:
            continue
        if 'zip' in f:
            continue
        filename = f.split('.')[0]
        year = int(meta_dict[filename][0])
        decade_class = (year % 1960) // 10
        if year < 1960:
            continue
        inf = open(test_path + f, "r", encoding='mac_roman')
        art = inf.read()
        test_data.append(art)
        test_target.append(decade_class)
        num_test += 1

    
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(train_data, train_target)
    labels = model.predict(test_data)

    print("# of articles trained:" + str(num_train))
    print("# of articles tested:" + str(num_test))

    print("Accuracy: " + str(accuracy_score(test_target, labels)))
    mat = confusion_matrix(test_target, labels)
    sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=[1960,1970,1980,1990,2000,2010], yticklabels=[1960,1970,1980,1990,2000,2010])
    plt.xlabel('true label')
    plt.ylabel('predicted label');
    plt.show()

    
classifyDecade()
