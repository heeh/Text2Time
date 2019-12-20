import numpy as np

preds_and_raw_dir = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/all_data/errorAnalysis/'
test_data_dir = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/all_data/dataset1960to2019/'

preds = np.load(preds_and_raw_dir + '/savenp_preds.npy')
raw = np.load(preds_and_raw_dir + '/savenp_raw.npy')
data = open(preds_and_raw_dir + 'test.csv', 'r', encoding='utf8', errors='ignore')

# data_len = 0
#
# for l in data:
#     data_len += 1
#
# data.close()
# data = open(preds_and_raw_dir + 'test.csv', 'r', encoding='utf8', errors='ignore')
#
# lengths = [len(preds), len(raw), data_len]
#
# if all(x == lengths[0] for x in lengths):
#     print('all equal')
#
# print(lengths)

c = 0

labal_mapping_inverse = {5: 9, 4: 8, 3: 7, 2: 6, 1: 1, 0: 0}

out_f = open(preds_and_raw_dir + 'incorrectlyPredictedArticlesWithDistance.txt', 'w+', encoding='utf8', errors='ignore')

keywords = ['trump', 'Trump', 'obama', 'Obama', '9/11',
            'recession', 'nixon', 'Nixon', 'clinton', 'Clinton', 'vietnam', 'Vietnam',
            'y2k', 'Y2K', 'AIDS', 'aids', 'Iraq', 'iraq', 'smartphone', 'radio', 'cassette']
run_type = 'gen_stats_with_keywords'
num_examples = 100
error_dists = np.empty([])

for p, r, d in zip(preds, raw, data):
    p = labal_mapping_inverse[p]
    r = labal_mapping_inverse[r]
    if run_type == 'keywords':
        for kw in keywords:
            if p != r and kw in d.split():
                out_f.write('predicted: ' + str(labal_mapping_inverse[p])
                            + '\nground truth: ' + str(labal_mapping_inverse[r]) + '\n')
                out_f.write('keyword: ' + str(kw) + '\n')
                out_f.write(d + '\n\n')
                c += 1
                break
    elif run_type == 'gen_stats_with_keywords':
        if abs(p - r) > 1:
            print(p)
            print(r)
            print(abs(p - r))
            print('....')
            error_dists = np.append(error_dists, abs(p - r))
            out_f.write('predicted: ' + str(p)
                        + '\nground truth: ' + str(r) + '\n')
            out_f.write('keyword: ' + '\n')
            out_f.write(d + '\n\n')
            c += 1
    elif run_type == 'basic':
        if p != r:
            out_f.write('predicted: ' + str(labal_mapping_inverse[p]) + '\nground truth: ' + str(
                labal_mapping_inverse[r]) + '\n')
            out_f.write(d + '\n\n')
            c += 1
    elif run_type == 'gen_stats':
        if p != r:
            error_dists = np.append(error_dists, abs(p - r))

    # if c > num_examples:
    #     break

if run_type == 'gen_stats' or run_type == 'gen_stats_with_keywords':
    print('average error distance: ' + str(np.average(error_dists)))
    print('error distance standard deviation: ' + str(np.std(error_dists)))

out_f.close()
data.close()
