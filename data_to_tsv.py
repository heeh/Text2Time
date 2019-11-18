# convert .data files to .tsv files

#
data_dir = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/dataset_raw/'
m = open(data_dir + 'meta.csv', 'r')
t = open('C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/dataset.tsv', 'w+', encoding='utf8')

# loop over meta data and grab four columns for tsv file
for row in m :
    columns = row.split(',')
    id = columns[0]
    label = columns[1]
    alpha = 'a'
    raw_f = open(data_dir + id + '.data', 'r', encoding='utf8')
    text = raw_f.read()
    raw_f.close()
    s = (id + '\t'
            + label + '\t'
            + alpha + '\t'
            + text.replace('\n', '') + '\n')
    t.write(s)
t.close()
m.close()
