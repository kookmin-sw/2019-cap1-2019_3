# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import re
import json
import pandas as pd                       
from urllib.parse import urljoin        
from google.cloud import translate
from google.cloud import storage
import google.auth
import sys
headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'), 
}
def spellchecker(comment_list):
    emoticon_list = ["❤️","🧡","💛","💚","💙","💞","💓","💜","❣️","💕","💘","💗","💓","💝","💟","😻","💔","👍","👎","🙌","😘","😍","😃","😄","😁","😆","☺️","😊","😚","🤗","😭","😢","😤","😠","😡","🤬","😳","🤔"]
    emotion_list = [" 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 사랑해요"," 싫어해요"," 최고에요","최악이에요","만세"," 사랑해요"," 사랑해요"," 좋아요"," 좋아요"," 좋아요"," 좋아요"," 좋아요"," 좋아요"," 좋아요"," 좋아요"," 슬퍼요"," 슬퍼요"," 삐졌어요"," 화났어요"," 화났어요"," 화났어요"," 잘 모르겠어요"," 고민해 볼게요"]

    module_path=os.path.join(os.path.dirname(os.path.abspath( __file__ ) ), '')
    sys.path.append(module_path)
    translate_client = translate.Client.from_service_account_json(module_path+'My First Project-c7d91da15e20.json')

    hangul = re.compile('[^ ㄱ-ㅣ가-힣A-Za-z?!]+')

    for comment_key in comment_list:
        row = comment_list[comment_key]['comment']
        comment = row.replace('\ufeff', '')
        if(len(comment)) < 500:
            url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy?'
            params = {}
            params['_callback'] = 'jQuery112409312646700220539_1557421638284'
            params['q'] = comment
            params['where'] = "nexearch"
            params['color_blindness'] = 0
            params['_'] = 1557292527466

            response = requests.get(url,params=params).text
            response = response.replace(params['_callback'] + '(','')
            response = response.replace(');','')
            try:
                response_dict = json.loads(response)

                result_text = response_dict['message']['result']['html']
                result_text = re.sub(r'<\/?.*?>','',result_text)
                #removed_emoji = hangul.sub('', result_text)
                removed_emoji = result_text
                translation = translate_client.translate(removed_emoji, target_language='ko')
                translated_sentence = translation['translatedText']
                for i in range(0,len(emoticon_list)):
                    translated_sentence = translated_sentence.replace(emoticon_list[i],emotion_list[i])
                comment_list[comment_key]['cor_comment'] = translated_sentence
            except:
                comment_list[comment_key]['cor_comment'] = comment

        else:
            comment_list[comment_key]['cor_comment'] = comment
   
    return comment_list

if __name__ == '__main__':
    line = "저여자 뭐임."
    print("수정결과 : " + spellchecker(line))




