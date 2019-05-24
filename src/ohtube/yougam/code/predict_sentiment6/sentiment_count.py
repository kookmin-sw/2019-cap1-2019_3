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


def predict_senti6(comment_list):

  currentPath = os.getcwd()

  module_path=os.path.join(os.path.dirname(os.path.abspath( __file__ ) ), '')
  sys.path.append(module_path)
  filename = module_path+"dataset/test_dataset_bow.pkl"
  with open(filename, "rb") as fp:
      X_test, Y_test, labels2names, text2features = pickle.load(fp)

  filename2 = module_path+"dataset/trained_model_gboost2.pkl"
  with open(filename2, "rb") as fp:
    net = pickle.load(fp)

  translate_client = translate.Client.from_service_account_json(module_path+'My First Project-c7d91da15e20.json')
  hangul = re.compile('[^ ㄱ-ㅣ가-힣A-Za-z?!]+')


  for comment_key in comment_list:

      emoticon_list = ["❤️","🧡","💛","💚","💙","💞","💓","💜","❣️","💕","💘","💗","💓","💝","💟","😻","💔","👍","👎","😘","😍","😃","😄","😁","😆","☺️","😊","😚","🤗","😭","😢","😤","😠","😡","🤬","😳","🤔"]
      emotion_list = [" love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," love you."," hate."," it is best."," hate."," love you."," love you."," it is good."," it is good."," it is good."," it is good."," it is good."," it is good."," it is good."," it is good."," it is sad."," it is sad."," not really."," hate."," hate."," hate."," i don't know"," i'll try."]

      row = comment_list[comment_key]['comment']
      comment = row.replace('\ufeff', '')
      print("cc",comment)
      if len(comment) < 2:
        comment_list[comment_key]['label'] = 'neutral'
        print("commenbt:,",comment)
        continue
      removed_emoji = comment

      if len(removed_emoji) >= 2:
        
        for i in range(0,len(emoticon_list)):
                removed_emoji = removed_emoji.replace(emoticon_list[i],emotion_list[i])

        translation = translate_client.translate(removed_emoji, target_language='en')
        translated_sentence = translation['translatedText']

        translated_sentence = translated_sentence.replace('&#39;',"'")

        print("popp",translated_sentence)
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
