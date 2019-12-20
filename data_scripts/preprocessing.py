import pandas as pd
from random import shuffle
from shutil import copyfile
import re
from collections import defaultdict
import pickle
import os

def split_dataset():

    meta = pd.read_csv(open('dataset1960to2019/meta1960to2019.data'), sep=',  ')

    id = meta['ID']
    year = meta['Year']
    month = meta['Month']

    curr_year = year[0]
    curr_month = month[0]

    curr_batch = []
    test_ids = []
    train_ids = []

    train_frac = 0.8    # Fraction of the dataset to be used for training, rest will be used for testing

    for i in range(len(meta)):
        print("Processing file ", i)
        if curr_year == year[i] and curr_month == month[i]:
            curr_batch.append(id[i])
        else:
            shuffle(curr_batch)
            num_train = int(len(curr_batch) * train_frac)
            train_ids += curr_batch[:num_train]
            test_ids += curr_batch[num_train:]
            curr_batch = [id[i]]
            curr_year = year[i]
            curr_month = month[i]

    if len(curr_batch) > 0:
        shuffle(curr_batch)
        num_train = int(len(curr_batch) * train_frac)
        train_ids += curr_batch[:num_train]
        test_ids += curr_batch[num_train:]

    for id in train_ids:
        copyfile('dataset1960to2019/data/'+str(id)+'.data', 'dataset1960to2019/train/'+str(id)+'.data')

    for id in test_ids:
        copyfile('dataset1960to2019/data/'+str(id)+'.data', 'dataset1960to2019/test/'+str(id)+'.data')

def clean_dataset():

    arr = ['Full text is unavailable for this digitized archive article. Subscribers may view the full text of this article in its original form through TimesMachine.',
           'Credit... The New York Times Archives',
            'NYTimes.com no longer supports Internet Explorer 9 or earlier. Please upgrade your browser.']

    meta = pd.read_csv(open('dataset1960to2019/meta1960to2019.data'), sep=',  ')
    id = meta['ID']

    for i in range(220949,len(meta)):
        try:
            print("Processing file ", i)
            f = open('dataset1960to2019/data/'+str(id[i])+'.data', 'r', encoding='utf8')
            contents = str(f.read())
            f.close()
            for s in arr:
                contents = contents.replace(s, '')
            f = open('dataset1960to2019/data/'+str(id[i])+'.data', 'w', encoding='utf8')
            f.write(contents)
            f.close()
        except:
            print("Error in ", i)
            continue

def remove_publishing_dates():

    #pat = '(January|February|March|April|May|June|July|August|September|October|November|December) (\\d|\\d\\d), (19|20)\\d\\d'
    pat = '(19|20)\\d\\d'

    meta = pd.read_csv(open('dataset1960to2019/meta1960to2019.data'), sep=',  ')
    id = meta['ID']

    for i in range(len(meta)):
        try:
            print("Processing file ", i)
            f = open('dataset1960to2019/data/' + str(id[i]) + '.data', 'r', encoding='utf8')
            contents = str(f.read())
            f.close()
            contents = re.sub(pat, '', contents)
            f = open('dataset1960to2019/data/' + str(id[i]) + '.data', 'w', encoding='utf8')
            f.write(contents)
            f.close()
        except:
            print("Error in ", i)
            continue

def get_category_counts():

    if os.path.exists('category_counts.pkl'):
        with open('category_counts.pkl', 'rb') as fp:
            ret = pickle.load(fp)
        return ret

    meta = pd.read_csv(open('dataset1960to2019/meta1960to2019.data'), sep=',  ')

    id = meta['ID']
    year = meta['Year']
    month = meta['Month']
    category = meta['Category']

    curr_year = year[0]
    curr_month = month[0]

    d = defaultdict(int)
    decade_count = {'1960': defaultdict(int), '1970': defaultdict(int), '1980': defaultdict(int), '1990': defaultdict(int),
                    '2000': defaultdict(int), '2010': defaultdict(int)}
    word_count = {'1960': defaultdict(list), '1970': defaultdict(list), '1980': defaultdict(list), '1990': defaultdict(list),
                    '2000': defaultdict(list), '2010': defaultdict(list)}


    for i in range(len(meta)):
        try:
            print("Processing file ", i)
            d[category[i]] += 1
            decade_count[str((year[i]//10) * 10)][category[i]] += 1
            f = open('dataset1960to2019/data/' + str(id[i]) + '.data', 'r', encoding='utf8')
            contents = str(f.read())
            f.close()
            word_count[str((year[i]//10) * 10)][category[i]].append(len(contents.split()))
        except:
            print("Error in ",i)
            continue

    with open('category_counts.pkl', 'wb') as fp:
        pickle.dump((d, decade_count, word_count), fp)

    return (d, decade_count, word_count)



#split_dataset()

#remove_publishing_dates()

c, decade_count, word_count = get_category_counts()

temp = [(k, c[k]) for k in c]

temp = sorted(temp, key=lambda x:x[1], reverse=True)

print(temp[:20])
