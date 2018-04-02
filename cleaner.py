from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymorphy2 import tokenizers
import nltk, string, json, pymorphy2
import pandas as pd

p_data = pd.read_json(open('good.json'))
n_data = pd.read_json(open('bad.json'))

dataset = pd.concat([p_data, n_data])
dataset = dataset[[1, 2]]

dataset.columns = ['text', 'label']

morph = pymorphy2.MorphAnalyzer()

def tokenize_me(file_text):
    file_text = file_text.lower()
    tokens = tokenizers.simple_word_tokenize(file_text)

    tokens = [morph.parse(w)[0].normal_form for w in tokens]

    #deleting punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]
  
    #deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', '...'])
    tokens = [i for i in tokens if (i not in stop_words)]

    return ' '.join(tokens)

dataset['text'] = dataset['text'].apply(tokenize_me)
dataset.to_csv('cleaned_data.csv')