import nltk
import keras
import json
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import numpy as np
import csv
import os
import sys
from konlpy.tag import Okt
from os import path

module_dir = os.path.dirname(__file__)  # get current directory
train_path = os.path.join(module_dir, 'train_docs.json')
model_path = os.path.join(module_dir, 'comment_model.h5')

def labeling(dic):
	okt = Okt()
	comment_dict = {}

	with open(train_path) as f:
		train_docs = json.load(f)
	tokens = [t for d in train_docs for t in d[0]]

	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
			model = load_model(model_path)

	text = nltk.Text(tokens, name='NMSC')
	selected_words = [f[0] for f in text.vocab().most_common(15000)]

	labels = {}
	for i in range(1,len(dic)+1):
		cmt = dic[i]
		grade = predict_pos_neg(cmt,selected_words,model)
		labels[i] = grade
	return labels

def tokenize(doc):
	okt = Okt()
	return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

def term_frequency(doc,selected_words):
	return [doc.count(word) for word in selected_words]

def predict_pos_neg(review,selected_words,model):
	token = tokenize(review)
	tf = term_frequency(token,selected_words)
	data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
	score = float(model.predict(data))

	if(score >= 0.8):
		score = 2
	elif(score <= 0.2):
		score = 0
	else:
		score = 1
	return score
