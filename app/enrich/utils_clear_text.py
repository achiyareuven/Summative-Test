import nltk
import os
nltk.data.path.append("./nltk_data")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def to_list_pairs_words(text):
    pairs_words = []
    for i in range(len(text) - 1):
        pairs_words.append(f"{text[i]} {text[i + 1]}")

    return pairs_words

def removing_stopwords(text):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    filtered_words = [w for w in tokens if w.lower() not in stop_words]
    clean_text = ' '.join(filtered_words)
    return clean_text


