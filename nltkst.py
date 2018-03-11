from nltk.stem.snowball import RussianStemmer
from nltk.corpus import stopwords
import nltk, string, json

st = RussianStemmer()

def tokenize_me(file_text):
    #applying nltk tokenization
    tokens = nltk.word_tokenize(file_text)

    #deleting punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]

    #deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    tokens = [i for i in tokens if (i not in stop_words)]

    #cleaning words
    tokens = [i.replace('«', '').replace('»', '') for i in tokens]

    return tokens

with open('keywords.txt') as fin:
	ww = fin.read().split(', ')
	key_words = list(set([st.stem(w) for w in ww]))



with open('test2.json') as fin:
	text = json.load(fin)

with open('bad.json', 'a') as fout:
	for dd in text:
		#for d in dd:
		words = tokenize_me(dd['description'])
		split_text = list(set([st.stem(word) for word in words]))
		#break
		tt = list(filter(lambda w: w in key_words, split_text))
		if tt:
			json.dump(dd, fout)
			fout.write('\n')