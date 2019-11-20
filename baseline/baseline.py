import re
import sys
import os
import typing
import nltk
import math
nltk.download('stopwords')
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from nltk.corpus import stopwords   
from nltk.tokenize import word_tokenize   


path = os.getcwd() + "/dataset/"


DIFF_RANGE = 60
#DIFF_RANGE = 6


tokenizer = nltk.data.load
meta_dict = Counter()
s_dict = []
pred_dict = Counter()
custom_dict = Counter()
def createDistribution() -> None:
    print('createDistribution()')
    inf = open(path + "meta.csv")
    lines = inf.readlines()

    # id -> [YYYY, MM, CATEGORY]
    for i in range(len(lines)):
        target = lines[i].replace(',','')
        target = target.rstrip('\n').split()
        meta_dict[target[0]] = target[1:]

    # for k,v in meta_dict.items():
    #     print(k,v)
    
    w_dict = []
    for i in range(DIFF_RANGE):
        w_dict.append(Counter())

    train_path = os.getcwd() + "/text2time_train/"
    # word - occurence dictionary: i = (YYYY % 1960) // 10
    for f in os.listdir(train_path):
        if 'csv' in f:
            continue
        if 'zip' in f:
            continue
        filename = f.split('.')[0]
        year = int(meta_dict[filename][0])
        if year < 1960:
            continue
        inf = open(path + f, "r")
        lines = inf.readlines()
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            stop_words = set(stopwords.words('english'))
            filtered_words = []   
            for w in target:
                w = w.lower()
                w = re.sub('[^a-zA-Z]+','',w)
                if w and w not in stop_words:   
                    filtered_words.append(w)   

            #Diff by decades
#            idx = (int(year) % 1960) // 10
            
            #Diff by Year
            idx = int(year) % 1960
            w_dict[idx].update(filtered_words)

        i = 0

    # Frequency Dictionary: i = (YYYY % 1960) // 10
    f_dict = []
    for i in range(DIFF_RANGE):
        f_dict.append(defaultdict(float))
    num_words = []
    
    for i in range(DIFF_RANGE):
        num_words.append(sum(w_dict[i].values()))

    for i in range(DIFF_RANGE):
        for k, v in w_dict[i].items():
            f_dict[i][k] = v / num_words[i]


    # for k,v in f_dict[0].items():
    #     if i == 30:
    #         return
    #     print(k,v)
    #     i += 1

    # i = (YYYY % 1960) // 10

    for i in range(DIFF_RANGE):
        s_dict.append(defaultdict(float))
    # General cases(1961s - 2018)
    for i in range(1,DIFF_RANGE-1):
        for k,v in f_dict[i].items():
            nextYear = f_dict[i+1].get(k, 0)
            currYear = f_dict[i].get(k,0)
            prevYear = f_dict[i-1].get(k,0)

            numerator = abs(nextYear - currYear) + abs(currYear - prevYear)
            denominator = prevYear + currYear + nextYear
            if denominator == 0:
                continue

            log_sum = abs(math.log(denominator))
            s_dict[i][k] = log_sum * (numerator / denominator)

    # Boundary cases(1960)
    for k,v in f_dict[0].items():
        nextYear = f_dict[1].get(k, 0)
        currYear = f_dict[0].get(k,0)

        numerator = abs(nextYear - currYear)
        denominator = currYear + nextYear
        if denominator == 0:
            continue
        log_sum = abs(math.log(denominator))
        s_dict[0][k] = log_sum * (numerator / denominator)

        
    # Boundary cases(2019)
    for k,v in f_dict[DIFF_RANGE-1].items():
        currYear = f_dict[DIFF_RANGE-1].get(k,0)
        prevYear = f_dict[DIFF_RANGE-2].get(k,0)
        
        numerator = abs(currYear - prevYear)
        denominator = prevYear + currYear
        if denominator == 0:
            continue

        log_sum = abs(math.log(denominator))
        s_dict[DIFF_RANGE-1][k] = log_sum * (numerator / denominator)




    # for i in range(DIFF_RANGE):
    #     print("-------------------------------------------------------")
    #     print('%d Highest word-frequency-diff TOP 10' % (i + 1960))
    #     print("-------------------------------------------------------")
    #     sorted_s_dict = sorted(s_dict[i].items(), key=lambda x : x[1], reverse=True)
    #     i = 0
    #     for k,v in sorted_s_dict:
    #         if i > 10:
    #             break
    #         print('%15s %.4f' % (k,v))
    #         i+=1



def showDistributionByYear():
    print('showDistributionByYear()')
    # Test
    start_year = 2007
    end_year = 2016

    for i in range(start_year - 1960, end_year - 1960):
        custom_dict.update(s_dict[i])


    print("-------------------------------------------------------")
    print('TOP 20(%d ~ %d)' % (start_year, end_year))
    print("-------------------------------------------------------")
    sorted_s_dict = sorted(custom_dict.items(), key=lambda x : x[1], reverse=True)
    i = 0
    for k,v in sorted_s_dict:
        if i > 20:
            break
        print('%15s %.4f' % (k,v))
        i+=1

    
    while(True):
        print("-------------------------------------------------------")
        print("This program takes starting and ending year and prints out top 20 highest fluctuated words.Type years within range from 1960 to 2019")
        start_year = int(input("Enter starting year in YYYY format: "))
        end_year   = int(input("Enter ending year in YYYY format: "))

        # start_year = 2007
        # end_year = 2016

        custom_dict = Counter()
        for i in range(start_year - 1960, end_year - 1960):
            custom_dict.update(s_dict[i])


        print("-------------------------------------------------------")
        print('TOP 20(%d ~ %d)' % (start_year, end_year))
        print("-------------------------------------------------------")
        sorted_s_dict = sorted(custom_dict.items(), key=lambda x : x[1], reverse=True)
        i = 0
        for k,v in sorted_s_dict:
            if i > 20:
                break
            print('%15s %.4f' % (k,v))
            i+=1

'''
input : meta.csv, test files
output: a dictionary of a file and a predicted year
'''
def predict():
    print("predict()")
    test_path = os.getcwd() + "/text2time_test/"
#    test_path = os.getcwd() + "/sample_test/"

    
    for f in os.listdir(test_path):
        if 'csv' in f:
            continue
        if 'zip' in f:
            continue
        filename = f.split('.')[0]
        year = int(meta_dict[filename][0])
        if year < 1960:
            continue

        meta = meta_dict[filename]
        # Retrieve label
        target_year = int(meta[0])

        # Compute prediction
        inf = open(path + f, "r")
        lines = inf.readlines()
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            stop_words = set(stopwords.words('english'))
            filtered_words = []   
            for w in target:
                w = w.lower()
                w = re.sub('[^a-zA-Z]+','',w)
                if w and w not in stop_words:   
                    filtered_words.append(w)   

        # Prediction by year
        # predictions = [0.0] * DIFF_RANGE
        # for i in range(DIFF_RANGE):
        #     for x in filtered_words:
        #         predictions[i] += s_dict[i][x]

        # Prediction by decade
        predictions = [0.0] * 6
        for i in range(6):
            for j in range(10):
                for x in filtered_words:
                    predictions[i] += s_dict[i*10+j][x]

        maxidx, maxscore = max(enumerate(predictions), key=lambda x: x[1])
        pred_dict[filename] = maxidx + 1960
    
    write_path = os.getcwd() + "/output/"
    write_file = open(write_path + "year_prediction.data", "w+")
    for k,v in pred_dict.items():
        write_file.write(k + ' ' + str(v))
        write_file.write('\n')


def compare():
    print("compare()")
    write_path = os.getcwd() + "/output/"
    write_file = open(write_path + "diff.data", "w+")
    write_file.write('ID\t pred \t actual \t correct\n')
    num_keys = 0
    num_trues = 0
    for k,v in pred_dict.items():
        pred = v
        actual = meta_dict[k][0]
        correct = (int(pred) <= int(actual) <= int(pred) + 10)
        if correct:
            num_trues += 1
        write_file.write(k + '\t' + str(pred) + '\t' + str(actual) + '\t' + str(correct))
        write_file.write('\n')
        num_keys += 1
    print('# of documents: ' + str(num_keys))
    print('Correct prediction: ' + str(num_trues))
    print('Probability: ' + str(num_trues / num_keys * 100))
    
    
    
createDistribution()
#showDistributionByYear()
predict()

compare()
