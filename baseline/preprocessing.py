import sys
import pandas as pd
from random import shuffle
from shutil import copyfile


SOURCE_DIR = 'big/'
META_DIR = 'big/meta.csv'
TRAIN_DIR ='big_train/'
TEST_DIR = 'big_test/'

#SOURCE_DIR = 'dataset/'
#META_DIR = 'dataset/meta.csv'
#TRAIN_DIR ='train_sample/'
#TEST_DIR = 'test_sample/'



def split_dataset():
    meta = pd.read_csv(open(META_DIR), sep=",  ")

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

    print("started copying data from"  + SOURCE_DIR+ "to" + TRAIN_DIR)
    for id in train_ids:
        copyfile(SOURCE_DIR+str(id)+'.data', TRAIN_DIR +str(id)+'.data')
    print("Finished copying data from"  + SOURCE_DIR+ "to" + TRAIN_DIR)
    
    print("started copying data from"  + SOURCE_DIR+ "to" + TEST_DIR)
    for id in test_ids:
        copyfile(SOURCE_DIR+str(id)+'.data', TEST_DIR+str(id)+'.data')
    print("Finished copying data from"  + SOURCE_DIR+ "to" + TEST_DIR)
split_dataset()
