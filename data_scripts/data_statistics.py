from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_common_words(corpus):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(corpus)
    filtered_corpus = [w for w in word_tokens if w not in stop_words]

    print('done filtering corpus...')

    return filtered_corpus


def get_top_n_words(corpus, n=None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.

    get_top_n_words(["I love Python", "Python is a language programming", "Hello world", "I love the world"]) ->
    [('python', 2),
     ('world', 2),
     ('love', 2),
     ('hello', 1),
     ('is', 1),
     ('programming', 1),
     ('the', 1),
     ('language', 1)]
    """
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


filename = 'C:/Users/Chase\'s Laptop/Downloads/train.csv'

file = open(filename, 'r', encoding='utf8')

w_sum = 0
count = 0
corpus = []
longest = ''
shortest = 'x ' * 210

for line in file:
    w_sum += len(line)
    count += 1
    corpus.append(line[2:].split())
    if len(longest.split()) < len(line[2:].split()) :
        longest = line
    if len(line[2:].split()) < len(shortest.split()):
        shortest = line

file.close()

print('average length of line: ', w_sum/count)
print('length of shortest article: \n', len(shortest))
print(shortest)
print('length of longest article: \n', len(longest))
print(longest)

