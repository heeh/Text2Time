import os.path


def transfer_files_from(start_date, dir_start, dir_end):
    # globals
    global project_path
    global global_id
    global meta_final
    global debug

    # progress prints
    print('transfer files....')
    print('start_date: ', start_date)
    print('dir_start: ', dir_start)
    print('dir_end: ', dir_end)
    print('-----------')

    # open up meta for start_date to end_date
    cur_meta = open(project_path
                    + 'dataset' + str(dir_start) + 'to' + str(dir_end)
                    + '/meta' + str(dir_start) + 'to' + str(dir_end)
                    + '.data', 'r')

    # copy all files corresponding to current meta into final data directory
    for cur_line in cur_meta:
        # grab id and year from current meta
        line_data = cur_line.strip().split(',')
        cur_id = int(line_data[0])
        cur_year = int(line_data[1])

        # declare final file name with global id
        final_f_name = project_path + 'dataset1960to2019/data/' + str(global_id) + '.data'
        if debug:
            file_exists = os.path.isfile(final_f_name)  # only write new file if file does not already exist
        else:
            file_exists = False  # always write new file if not debugging

        if start_date <= cur_year and not file_exists:
            # write global meta data to final meta file
            line_data[0] = str(global_id)
            meta_final.write(', '.join(line_data) + '\n')

            # open up final file with global id (declared above)
            final_f = open(final_f_name, 'w+', encoding='utf8', errors='ignore')

            # grab file corresponding to current id
            old_f = open(project_path + 'dataset'
                         + str(dir_start) + 'to' + str(dir_end) + '/data/'
                         + str(cur_id) + '.data', 'r+', encoding='utf8', errors='ignore')

            # write old_f to final_file with global id
            final_f.write(old_f.read())

            final_f.close()
            old_f.close()
        elif cur_year < start_date:  # only used in 85-88 overlap
            break

        # increment global id
        global_id += 1

        # progress prints
        printing_it = 1000
        if global_id % printing_it == 0:
            print('global_id', global_id)
            print('cur_year', cur_year, '--------')

    cur_meta.close()
    print('')


# declare globals
project_path = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/'
meta_final = open(project_path + 'dataset1960to2019/meta1960to2019.data', 'w+')
global_id = 0
debug = False

# method calls assume that data directories all follow these rules:
# - outter data directory name is "dataset[start_date]to[end_date]
# - sit in same directory as this script
# - actual data files sit in inner directory called "data"
# - meta files are named "meta[start_date]to[end_date].data"
# - meta files sit in outter data directory
transfer_files_from(1988, 1985, 2019)  # '88 to '19
transfer_files_from(1983, 1983, 1988)  # '83 to '88
transfer_files_from(1975, 1975, 1982)  # '75 to '82
transfer_files_from(1973, 1973, 1975)  # '73 to '75
transfer_files_from(1960, 1960, 1973)  # '60 to '73

meta_final.close()
