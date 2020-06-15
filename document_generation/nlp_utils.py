import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer


def pre_processing(text):
    """
    note the stemming step has been removed specially for this project
    :param text: the text to be treated
    :return:
    """

    # replacing punctuations with empty spaces
    text2 = " ".join("".join([" " if ch in string.punctuation else ch for ch in text]).split())

    # tokenizing the text to words, after being converted to sentences
    tokens = [word for sent in nltk.sent_tokenize(text2) for word in nltk.word_tokenize(sent)]

    # converting all words to lower case
    tokens = [word.lower() for word in tokens]

    # removal of stop words
    stops = stopwords.words('french')
    tokens = [token for token in tokens if token not in stops]

    # removing words less than 2 characters
    tokens = [word for word in tokens if len(word) >= 2]

    return tokens
