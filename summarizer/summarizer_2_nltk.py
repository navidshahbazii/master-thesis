import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import warnings
from nltk.corpus import stopwords
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.max_colwidth = 100

file = pd.read_excel('input.xlsx')
# file = file.drop(file.index[842])
# test_value = file.abstract.values[842]
# print(test_value)

nltk.download('stopwords')

HANDICAP = 0.80


def remove_punctuation_marks(text):
    punctuation_marks = dict((ord(punctuation_mark), None) for punctuation_mark in string.punctuation)
    return text.translate(punctuation_marks)


def get_lemmatized_tokens(text):
    normalized_tokens = nltk.word_tokenize(remove_punctuation_marks(text.lower()))
    return [nltk.stem.WordNetLemmatizer().lemmatize(normalized_token) for normalized_token in normalized_tokens]


def get_average(values):
    greater_than_zero_count = total = 0
    for value in values:
        if value != 0:
            greater_than_zero_count += 1
            total += value
    return total / greater_than_zero_count if greater_than_zero_count != 0 else 0


def get_threshold(tfidf_results):
    i = total = 0
    while i < (tfidf_results.shape[0]):
        total += get_average(tfidf_results[i, :].toarray()[0])
        i += 1
    return total / tfidf_results.shape[0]


def get_summary(documents, tfidf_results):
    summary = ""
    i = 0
    while i < (tfidf_results.shape[0]):
        if (get_average(tfidf_results[i, :].toarray()[0])) >= get_threshold(tfidf_results) * HANDICAP:
            summary += ' ' + documents[i]
        i += 1
    return summary


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print('punkt')
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    file['summary_nltk'] = ''
    for i in range(1000):
        documents = nltk.sent_tokenize(file.abstract[i])
        tfidf_results = TfidfVectorizer(tokenizer=get_lemmatized_tokens,
                                        stop_words=stopwords.words('english')).fit_transform(documents)
        print('before: ', documents)
        file['summary_nltk'][i] = get_summary(documents, tfidf_results)
        print('after: ', file['summary_nltk'][i])

    file.to_excel("output_nltk.xlsx", index = False)