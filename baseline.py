import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict


path = os.getcwd() + "/dataset/"


def baseline() -> None:
    inf = open(path + "meta.csv")
    lines = inf.readlines()

    # id -> [YYYY, MM, CATEGORY]
    meta_dict = Counter()
    for i in range(len(lines)):
        target = lines[i].replace(',','')
        target = target.rstrip('\n').split()
        meta_dict[i] = target[1:]

    # for k,v in meta_dict.items():
    #     print(k,v)
    
    wc = []

    for i in range(6):
        wc.append(Counter())
    
    for f in os.listdir(path):
        if 'csv' in f:
            continue
        if 'zip' in f:
            continue
        filename = f.split('.')[0]
 
        year = int(meta_dict[int(filename)][0])
        if year < 1960:
            continue
        inf = open(path + f, "r")
        lines = inf.readlines()
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            idx = (int(year) % 1960) // 10
            # print(year)
            # print(idx)
            wc[idx].update(target)
#    print(wc[0])
baseline()

