import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.max_colwidth = 100
from nltk.stem import PorterStemmer
from num2words import num2words
import numpy as np
from gensim.parsing.preprocessing import remove_stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stops = set(stopwords.words("english"))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


file = pd.read_excel('input_13.04.2021.xlsx')

################### Clustering: ###################
file['Abstract'] = file.abstract

def convert_lower_case(data):
    data['Abstract'] = data['Abstract'].str.lower()
    return data


def remove_stop_words(data):
    for i in range(1000):
        data['Abstract'][i] = remove_stopwords(data['Abstract'][i])
    return data


def remove_punctuation(data):
    spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")",
                  "*", "+", ",", "-", ".", "/", ":", ";", "<",
                  "=", ">", "?", "@", "[", "\\", "]", "^", "_",
                  "`", "{", "|", "}", "~", "$", "\n"]
    for char in spec_chars:
        data['Abstract'] = data['Abstract'].str.replace(char, '')
    return data


def stemming(data):
    stemmer = PorterStemmer()
    for i in range(1000):
        tokens = word_tokenize(str(data.Abstract[i]))
        new_text = ""
        for w in tokens:
            new_text = new_text + " " + stemmer.stem(w)
        data.Abstract[i] = new_text
    return data


def convert_numbers(data):
    for i in range(1000):
        tokens = word_tokenize(str(data.Abstract[i]))
        new_text = ""
        for w in tokens:
            try:
                w = num2words(int(w))
            except:
                a = 0
            new_text = new_text + " " + w
        new_text = np.char.replace(new_text, "-", " ")
        data.Abstract[i] = new_text
    return data


def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)  # remove comma separately
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data)  # needed again as we need to stem the words
    data = remove_punctuation(data)  # needed again as num2word is giving few hyphens and commas fourty-one
    data = remove_stop_words(data)  # needed again as num2word is giving stop words 101 - one hundred and one
    return data
file = preprocess(file)

#  calculating TF-IDF:


articles = list(file['Abstract'])

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(articles)
df = pd.DataFrame(X[0].T.todense(), index=vectorizer.get_feature_names(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=False)
print(df.head(25))

#  Text Clustering:


true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=10)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
print(terms)
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

file['cluster_nr'] = ''
file['cluster_key_terms'] = ''
for i in range(1000):
    Y = vectorizer.transform([file.Abstract[i]])
    file['cluster_nr'][i] = model.predict(Y)
    if file.cluster_nr[i] == 0:
        for ind in order_centroids[0, :10]:
            file.cluster_key_terms[i] = file.cluster_key_terms[i] + " " + terms[ind]
    if file.cluster_nr[i] == 1:
        for ind in order_centroids[1, :10]:
            file.cluster_key_terms[i] = file.cluster_key_terms[i] + " " + terms[ind]
    if file.cluster_nr[i] == 2:
        for ind in order_centroids[2, :10]:
            file.cluster_key_terms[i] = file.cluster_key_terms[i] + " " + terms[ind]
    if file.cluster_nr[i] == 3:
        for ind in order_centroids[3, :10]:
            file.cluster_key_terms[i] = file.cluster_key_terms[i] + " " + terms[ind]
print(file.Abstract, file.cluster_nr)
# file.to_excel('clustering_outpu.xlsx', index=False)
del file['Abstract']
file.to_excel("clustering_output_13_04_2021.xlsx", index=False)