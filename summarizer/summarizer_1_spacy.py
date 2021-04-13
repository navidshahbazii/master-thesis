import spacy
import re
import pandas as pd
from collections import Counter
from string import punctuation
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.max_colwidth = 100

file = pd.read_excel('ACM_output.xlsx')
test_value = file['abstract'].values[4]

nlp = spacy.load('en_core_web_sm')

# Strip HTLM tags
# Citation: https://stackoverflow.com/a/925630
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Clean up line breaks, HTML tags, extra spaces, and first tone plural
def clean_text(text):
    # Citation: lrnq @ github for this space normalization step
    text = ' '.join(text.split())

    # Remove line breaks
    # Citation: https://stackoverflow.com/a/16566356
    text = text.replace('\n', ' ').replace('\r', '')

    # Strip HTML tags
    text = strip_tags(text)

    # Remove extra spaces
    # Citation: https://stackoverflow.com/a/1546244
    text = re.sub(' +', ' ', text)

    # Remove spaces before punctuation
    # Citation: https://stackoverflow.com/a/18878970
    text = re.sub(r'\s([?,.!"):;](?:\s|$))', r'\1', text)

    # Change "We" and "Our" etc
    text = text.replace('We ', 'The authors ')
    text = text.replace(' we ', ' the authors ')
    text = text.replace('Our ', 'The authors\' ')
    text = text.replace(' our ', ' the authors\' ')

    # Change "conlusion"
    text = text.replace('CONCLUSION:', 'In conclusion, ')
    text = text.replace('CONCLUSION ', 'In conclusion, ')
    text = text.replace('CONCLUSIONS:', 'In conclusion, ')
    text = text.replace('CONCLUSIONS ', 'In conclusion, ')
    text = text.replace('Conclusion:', 'In conclusion, ')
    text = text.replace('Conclusion ', 'In conclusion, ')
    text = text.replace('Conclusions:', 'In conclusion, ')
    text = text.replace('Conclusions ', 'In conclusion, ')
    text = re.sub(' +', ' ', text)

    return text


# Track case sensitive tokens
def track_case(text):
    cased_words = []
    ignore = ["BACKGROUND", "PURPOSE", "METHODS", "RESULTS", "CONCLUSION", "DISCUSSION", "AIMS", "INTRODUCTION", "AND",
              "ANALYSIS", "DESIGN", "ETHICS", "DISSEMINATION", "TRIAL", "REGISTRATION", "NUMBER", "CONCLUSIONS",
              "AIMS/INTRODUCTION", "MATERIALS", "STUDY", "TYPE", "POPULATION", "FIELD", "STRENGTH/SEQUENCE", "STRENGTH",
              "SEQUENCE", "ASSESSMENT", "STATISTICAL", "TESTS", "DATA", "LEVEL", "OF", "EVIDENCE", "OBJECTIVE", "MAIN",
              "KEY", "FINDINGS", "SIGNIFICANCE", "TRANSLATIONAL", "PERSPECTIVE"]
    doc = nlp(text)
    for token in doc:
        token = token.text
        if token != token.lower() and re.search('^[A-Z][a-z]+$', token) == None and len(
                token) > 1 and token not in ignore:
            cased_words.append(token)

    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace(':', ' ')
    text = text.replace(',', ' ')
    text = text.replace(';', ' ')

    # Since spaCy breaks terms with hypens, I go through the text again, with manual tokenization and identification of hypen tokens
    for token in text.split():
        if "-" in token and token != token.lower() and re.search('^[A-Z][a-z]+$', token) == None:
            cased_words.append(token)

    return set(cased_words)


def change(text, word):
    # Citation: lrnq @ github solution
    return ' '.join([x.replace(word.lower(), word) if x == word.lower()
                                                      or x == "(" + word.lower() + "),"
                                                      or x == "(" + word.lower() + ")."
                                                      or x == "(" + word.lower() + ");"
                                                      or x == "(" + word.lower() + "):"
                                                      or x == "(" + word.lower() + ")"
                                                      or x == word.lower() + ","
                                                      or x == word.lower() + "."
                                                      or x == word.lower() + ";"
                                                      or x == word.lower() + ":"
                     else x for x in text.split()])

def fix_case(text, case_list):
    for word in case_list:
        text = change(text, word)
    return text


def top_sentence(text, limit):
    '''
    Args:
        text - the input text
        limit - the number of sentences to return
    '''

    text = clean_text(text)
    cased = track_case(text)

    keyword = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    # to lower and tokenize
    doc = nlp(text.lower())

    # loop over the tokens
    for token in doc:

        # ignore stopword or punctuation
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # append definded POS words
        if (token.pos_ in pos_tag):
            keyword.append(token.text)

    # to normalize the weightage of the keywords
    freq_word = Counter(keyword)
    # get the frequency of the top most-common keyword
    max_freq = Counter(keyword).most_common(1)[0][1]
    # normalize the frequency
    for w in freq_word:
        freq_word[w] = (freq_word[w] / max_freq)

    # manually increase weight for conclusions and summary
    freq_word['conclusion'] = 10

    sent_strength = {}
    # loop over each sentence
    for sent in doc.sents:

        # loop over each word
        for word in sent:
            # decide if the word is a keyword
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    # add the normalized keyword value to the key-value pair of the sentence
                    sent_strength[sent] += freq_word[word.text]
                else:
                    # create new key-value in the sent_strength dic using sent as key and norm keyword value as value
                    sent_strength[sent] = freq_word[word.text]

    summary = []
    # sort the dic in descending order
    sorted_x = sorted(sent_strength.items(), key=lambda kv: kv[1], reverse=True)

    counter = 0
    # loop over each of sorted items
    for i in range(len(sorted_x)):
        # append result to the list
        summary.append(str(sorted_x[i][0]).capitalize())

        counter += 1
        if (counter >= limit):
            break

    result = ' '.join(summary)

    # fix the case
    result2 = fix_case(result, cased)

    return result2

print('initial text: ')
print(test_value)
print('final text: ')
print(top_sentence(test_value, 2))

