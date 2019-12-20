import pickle
from collections import defaultdict

folder = 'datasetByYears/datasetByYears'

toTry = ['0', '1', '6', '7', '8', '9']

d = defaultdict(list)

for year in toTry:
    idx = 0
    with open(folder+'/'+year+'_train.csv', 'r', encoding='utf8') as fp:
        for line in fp:
            try:
                print("Line ", idx+1, "of year ",year)
                idx += 1
                d[year].append(len(line[2:].split()))
            except:
                print("Error in file", idx+1)
    
    with open(folder+'/'+year+'_test.csv', 'r', encoding='utf8') as fp:
        for line in fp:
            try:
                print("Line ", idx+1, "of year ",year)
                idx += 1
                d[year].append(len(line[2:].split()))
            except:
                print("Error in file", idx+1)

with open('savefile', 'wb') as fp:
    pickle.dump(d, fp)