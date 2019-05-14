import csv
import pickle
import nltk
import json
import re
import mock
import os
from google.cloud import translate
from google.cloud import storage
import google.auth
import sys
# pip install --upgrade google-cloud-translate
# pip install --upgrade google-cloud-storage
# pip install google-auth
# pip install mock


def csvToDict(comment_list):

  currentPath = os.getcwd()
  os.chdir('C:/Users/ljj56/Desktop/Capstone/2019-cap1-2019_3/src/ohtube/yougam/code/predict_sentiment6')
  filename = "dataset/test_dataset_bow.pkl"
  with open(filename, "rb") as fp:
      X_test, Y_test, labels2names, text2features = pickle.load(fp)

  filename2 = "dataset/trained_model_gboost2.pkl"
  with open(filename2, "rb") as fp:
    net = pickle.load(fp)

  translate_client = translate.Client.from_service_account_json('My First Project-e23890f11bd3.json')
  hangul = re.compile('[^ ㄱ-ㅣ가-힣A-Za-z?!]+')


  for comment_key in comment_list:
      row = comment_list[comment_key]['comment']
      comment = row.replace('\ufeff', '')
      if len(comment) < 2:
        comment_list[comment_key]['label'] = 'neutral'
        continue
      removed_emoji = hangul.sub('', comment)
      if len(removed_emoji) > 2:
        translation = translate_client.translate(removed_emoji, target_language='en')
        translated_sentence = translation['translatedText']

        predict = labels2names[net.predict_from_sentence(translated_sentence.split(), text2features)]
        comment_list[comment_key]['label'] = predict

      else : comment_list[comment_key]['label'] = 'neutral'
  return comment_list







def sentenceCount(senti_dict):

    sentence_dict = senti_dict

    sentiment_count = {'neutral': 0, 'happy': 0, 'sad': 0, 'surprise':0, 'anger':0, 'fear': 0}
    for c in sentence_dict:
      label = sentence_dict[c]['label']
      sentiment_count[label] += 1


    return sentiment_count




if (__name__ == "__main__"):
    comment_list = {'1': {'comment':"이 영상 넘 재밌어요", 'author': 'leejinjoo', 'period':'3일 전'}, '2': {'comment':'가방은 어디서 샀나요?', 'author': 'juhyang', 'period':'1일 전'}, '3':{'comment':'영상이 너무 슬퍼요', 'author': 'jiyeon', 'period':'한달 전'}}
    # explicit()
