from konlpy.tag import Okt
import json
import nltk
import keras
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import numpy as np
import csv

def tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]
def term_frequency(doc):
    return [doc.count(word) for word in selected_words]
def predict_pos_neg(review):
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))

    if(score >= 0.8):
        print("긍정 입니다")
        score = 2
    elif(score <= 0.1):
        print("부정 입니다")
        score = 0
    else:
        print("중립 입니다")
        score = 1
    return score


def toJson(comment_dict):
	with open('comment.json','w',encoding = 'utf-8') as file:
		json.dump(comment_dict,file,ensure_ascii=False,indent='\t')

okt = Okt()
with open('data/train_docs.json') as f:
    train_docs = json.load(f)
tokens = [t for d in train_docs for t in d[0]]

with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model('data/comment_model.h5')

text = nltk.Text(tokens, name='NMSC')
selected_words = [f[0] for f in text.vocab().most_common(15000)]

# comment_dict = {}
# f = open('data/data.csv', 'r', encoding='utf-8') 
# rdr = csv.reader(f)
# size = 0
# for line in rdr:
#     size = size + 1
#     if len(str(line[1])) < 3:
#         continue
#     comment = line[1].replace('\ufeff','')
#     grade = predict_pos_neg(comment)
#     comment_dict[line[0]] = {'sentence':comment,'label':grade}
# comment_dict['len'] = size
# toJson(comment_dict)
while(1):
	a = input("문장을 입력하세요:")
	predict_pos_neg(a)
# predict_pos_neg("아 군침 돈다...쩝")
