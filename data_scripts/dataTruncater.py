
def truncate_f_to_len(f_to_trunc, trunc_len):
    print('truncating data in ', f_to_trunc, '...')

    in_train_file = open(f_to_trunc + 'train.csv', 'r', encoding='utf8')
    in_test_file = open(f_to_trunc + 'test.csv', 'r', encoding='utf8')

    out_train_file = open(f_to_trunc + 'train_truncated.csv', 'w+', encoding='utf8')
    out_test_file = open(f_to_trunc + 'test_truncated.csv', 'w+', encoding='utf8')

    # truncate train
    for line in in_train_file:
        tokens = line.split()

        # if line is shorter than average, don't use it
        # otherwise, truncate line
        if trunc_len < len(tokens):
            truncated_line = ' '.join(tokens[:trunc_len])
            out_train_file.write(truncated_line + '\n')

    # truncate test
    for line in in_test_file:
        tokens = line.split()

        if trunc_len < len(line):
            truncated_line = ' '.join(tokens[:trunc_len])
            out_test_file.write(truncated_line + '\n')

    in_train_file.close()
    in_test_file.close()
    out_train_file.close()
    out_test_file.close()

    print('done.')


def average_length_of_lines(filename):
    print('getting average line length from ', filename)

    data_f = open(filename, 'r', encoding='utf8')

    line_count = 0
    word_sum = 0

    for line in data_f:
        line_count += 1
        word_sum += len(line.split())

    data_f.close()

    print('done')

    return word_sum / line_count


full_data_dir = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/all_data/fullDataClean/'

avg_line_len = average_length_of_lines(filename=full_data_dir + 'train.csv')

print(avg_line_len)

truncate_f_to_len(f_to_trunc=full_data_dir, trunc_len=int(avg_line_len))

print(average_length_of_lines(filename=full_data_dir + 'train_truncated.csv'))
