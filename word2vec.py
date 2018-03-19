from sklearn.cross_validation import train_test_split
from gensim.models.word2vec import Word2Vec
from sklearn.preprocessing import scale
from sklearn.linear_model import SGDClassifier
import nltk, string, json
import numpy as np

def cleanText(corpus):
	reviews = []
	for dd in corpus:
		#for d in dd:
		try:
			words = nltk.word_tokenize(dd['description'])
			words = [w.lower() for w in words]
			reviews.append(words)
			#break
		except:
			pass
	return reviews

with open('bad.json') as fin:
	text = json.load(fin)
	neg_rev = cleanText(text)

with open('good.json') as fin:
	text = json.load(fin)
	pos_rev = cleanText(text)

#1 for positive sentiment, 0 for negative
y = np.concatenate((np.ones(len(pos_rev)), np.zeros(len(neg_rev))))

x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos_rev, neg_rev)), y, test_size=0.2)

n_dim = 1104
#Initialize model and build vocab
imdb_w2v = Word2Vec(size=n_dim, min_count=10)
imdb_w2v.build_vocab(x_train)

#Train the model over train_reviews
imdb_w2v.train(x_train, total_examples=imdb_w2v.corpus_count, epochs=imdb_w2v.iter)

#Build word vector for training set
def buildWordVector(text, size):
	vec = np.zeros(size).reshape((1, size))
	count = 0.
	for word in text:
		try:
			vec += imdb_w2v[word].reshape((1, size))
			count += 1.
		except KeyError:
			continue
	if count != 0:
		vec /= count
	return vec

train_vecs = np.concatenate([buildWordVector(z, n_dim) for z in x_train])
train_vecs = scale(train_vecs)

#Train word2vec on test reviews
imdb_w2v.train(x_test, total_examples=imdb_w2v.corpus_count, epochs=imdb_w2v.iter)

#Build test vectors then scale
test_vecs = np.concatenate([buildWordVector(z, n_dim) for z in x_test])
test_vecs = scale(test_vecs)

#Use classification algorithm 
lr = SGDClassifier(loss='log', penalty='l1')
lr.fit(train_vecs, y_train)

print('Test Accuracy: %.2f'%lr.score(test_vecs, y_test))