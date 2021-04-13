import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.max_colwidth = 100

file = pd.read_excel('ACM_output.xlsx')

# Build a List of Stopwords
stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')

def summarizer(document1):
    # Build an NLP Object
    docx = nlp(document1)

    # Tokenization of Text
    mytokens = [token.text for token in docx]

    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # Maximum Word Frequency
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    # Sentence Tokens
    sentence_list = [sentence for sentence in docx.sents]

    # Example of Sentence Tokenization,Word Tokenization and Lowering All Text
    [w.text.lower() for t in sentence_list for w in t]

    # Sentence Score via comparrng each word with sentence
    sentence_scores = {}
    for sent in sentence_list:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if len(sent.text.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Finding Top N Sentence with largest score
    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)

    # List Comprehension of Sentences Converted From Spacy.span to strings
    final_sentences = [w.text for w in summarized_sentences]

    # Join sentences
    summary = ' '.join(final_sentences)
    return summary

i=0
file['abstract_summary'] = ''
for i in range(1000):
    file['abstract_summary'][i] = summarizer(file.abstract[i])

file.to_excel("summarizer_3_spacy_output.xlsx", index=False)