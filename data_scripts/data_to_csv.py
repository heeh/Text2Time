import os

# convert multiple .data files into one csv file
# assumes we have raw .data files in local directory
def convert_to_csv(data_dir, write_to, split_type='all', debug_print=False):
    if debug_print:
        debug_counter = 0
        print_iter = 10000
        if split_type == 'all':
            print('convert_to_csv running on all')
        elif split_type == 'categories':
            print('convert_to_csv running on categories')

    # loop over meta data and grab four columns for csv file
    m = open(data_dir + 'meta1960to2019.data', 'r')  # currently have to manually change this meta name :(

    if split_type == 'all':
        t_dict = {'all': []}
    elif split_type == 'categories':
        t_dict = {}

    for row in m:
        columns = row.split(', ')
        ID = columns[0]
        label = columns[1].lstrip()[2]
        if split_type == 'categories':
            category = columns[3].rstrip().lstrip().replace('\"', '').replace(':', '')
            if category is not None and category not in t_dict.keys():
                t_dict[category] = []

        raw_f = open(data_dir + '/data/' + ID + '.data', 'r', encoding='utf8')
        text = raw_f.read()
        raw_f.close()
        s = label + ',' + text.replace('\n', '').replace(',', '') + '\n'
        if debug_print and debug_counter % print_iter == 0:
            print(s[:-1])

        if split_type == 'all':
            t_dict['all'].append(s)
        elif split_type == 'categories':
            t_dict[category].append(s)

        debug_counter += 1
    m.close()

    if debug_print:
        print('list creation done. Shuffling...')

    # shuffle
    from random import shuffle
    if split_type == 'all':
        shuffle(t_dict['all'])
    elif split_type == 'categories':
        for cat in t_dict.keys():
            shuffle(t_dict[cat])

    if debug_print:
        print('list shuffling done. Splitting...')

    # split
    if split_type == 'all':
        train_t = t_dict['all'][:int(len(t_dict['all']) * 0.8)]
        test_t = t_dict['all'][int(len(t_dict['all']) * 0.8):]
    elif split_type == 'categories':
        train_dict = {}
        test_dict = {}
        for cat in t_dict.keys():
            train_dict[cat] = t_dict[cat][:int(len(t_dict[cat]) * 0.8)]
            test_dict[cat] = t_dict[cat][int(len(t_dict[cat]) * 0.8):]

    if debug_print:
        print('list splitting done done. Writing...')

    # write
    if split_type == 'all':
        file_name = write_to + 'train.csv'
        if os.path.isfile(file_name) and debug_print:
            train_f = open(file_name, 'w+', encoding='utf8')
            for line in train_t:
                train_f.write(line)
            train_f.close()

        file_name = write_to + 'test.csv'
        if os.path.isfile(file_name) and debug_print:
            test_f = open(write_to + 'test.csv', 'w+', encoding='utf8')
            for line in test_t:
                test_f.write(line)
            test_f.close()
    elif split_type == 'categories':
        for cat in t_dict.keys():
            file_name = write_to + cat + '_train.csv'
            if os.path.isfile(file_name) and debug_print:
                train_f = open(write_to + cat + '_train.csv', 'w+', encoding='utf8')
                for line in train_dict[cat]:
                    train_f.write(line)
                train_f.close()

            file_name = write_to + cat + '_test.csv'
            if os.path.isfile(file_name) and debug_print:
                test_f = open(write_to + cat + '_test.csv', 'w+', encoding='utf8')
                for line in test_dict[cat]:
                    test_f.write(line)
                test_f.close()

    if debug_print:
        cat_file = open(write_to + 'allCategories.data', 'w+', encoding='utf8')
        for cat in t_dict.keys():
            cat_file.write(cat + '\n')
        cat_file.close()


full_data = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/all_data/dataset1960to2019/'
cat_data = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/all_data/datasetByCategories/'

convert_to_csv(data_dir=full_data, write_to=cat_data, split_type='categories', debug_print=True)
