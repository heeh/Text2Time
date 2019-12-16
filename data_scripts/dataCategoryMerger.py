import os


def merge_all_in(base_dir, inner_dir, debug_it=500000):
    debug_counter = 0
    raw_data_dir = base_dir + inner_dir + '/IndividualCSVs/'
    print(base_dir + inner_dir + '/' + inner_dir + 'MERGED_train.csv')
    final_train_f = open(base_dir + inner_dir + '/' + inner_dir + '_train.csv', 'w+', encoding='utf8')
    final_test_f = open(base_dir + inner_dir + '/' + inner_dir + '_test.csv', 'w+', encoding='utf8')

    for filename in os.listdir(raw_data_dir):
        if filename.endswith('csv'):
            if filename[-9:-4] == 'train':
                temp_train_f = open(raw_data_dir + filename, 'r', encoding='utf8')
                for line in temp_train_f:
                    if debug_counter % debug_it == 0:
                        print(line[:-1])
                    final_train_f.write(line)
                    debug_counter += 1
                temp_train_f.close()

            elif filename[-8:-4] == 'test':
                temp_test_f = open(raw_data_dir + filename, 'r', encoding='utf8')
                for line in temp_test_f:
                    if debug_counter % debug_it == 0:
                        print(line[:-1])
                    final_test_f.write(line)
                    debug_counter += 1
                temp_test_f.close()


cat_dir = 'C:/Users/Chase\'s Laptop/PycharmProjects/Text2Time/all_data/datasetByCategories/'

merge_all_in(base_dir=cat_dir, inner_dir='ArtFashionFoodAndWine')
merge_all_in(base_dir=cat_dir, inner_dir='BlogsOpEdsObits')
merge_all_in(base_dir=cat_dir, inner_dir='BooksAndMagazines')
merge_all_in(base_dir=cat_dir, inner_dir='BusinessAndFinance')
merge_all_in(base_dir=cat_dir, inner_dir='DomesticAndCulture')
merge_all_in(base_dir=cat_dir, inner_dir='International')
merge_all_in(base_dir=cat_dir, inner_dir='Lifestyle')
merge_all_in(base_dir=cat_dir, inner_dir='News')
merge_all_in(base_dir=cat_dir, inner_dir='ScienceEdAutosAndTech')
merge_all_in(base_dir=cat_dir, inner_dir='ShowsMoviesGamesAndEntertainment')
merge_all_in(base_dir=cat_dir, inner_dir='Sports')

