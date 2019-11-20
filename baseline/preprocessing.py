import pandas as pd
from random import shuffle
from shutil import copyfile

def split_dataset():

    meta = pd.read_csv(open('dataset/meta.data'), sep=', ')

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
        copyfile('dataset/'+str(id)+'.data', 'text2time_train/'+str(id)+'.data')

    for id in test_ids:
        copyfile('dataset/'+str(id)+'.data', 'text2time_test/'+str(id)+'.data')

split_dataset()