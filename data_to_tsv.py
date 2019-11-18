# convert .data files to .tsv files
# assumes we have raw .data files in local directory

# convert
# loop over meta data and grab four columns for tsv file
# put them in a list so we can shuffle and split
data_dir = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/dataset_raw/'
m = open(data_dir + 'meta.csv', 'r')
t_list = []
for row in m:
    columns = row.split(',')
    ID = columns[0]
    label = columns[1]
    alpha = 'a'
    raw_f = open(data_dir + ID + '.data', 'r', encoding='utf8')
    text = raw_f.read()
    raw_f.close()
    s = (ID + '\t'
            + label + '\t'
            + alpha + '\t'
            + text.replace('\n', '') + '\n')
    t_list.append(s)
m.close()

# shuffle
from random import shuffle
shuffle(t_list)

# split
train_t = t_list[:int(len(t_list) * 0.8)]
test_t = t_list[int(len(t_list) * 8):]

# write
train_f = open('C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/train.tsv', 'w+', encoding='utf8')
for line in train_t:
    train_f.write(line)
train_f.close()

test_f = open('C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/test.tsv', 'w+', encoding='utf8')
for line in test_t:
    test_f.write(line)
test_f.close()

