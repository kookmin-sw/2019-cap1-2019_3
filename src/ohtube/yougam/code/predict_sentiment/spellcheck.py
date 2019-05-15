
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import re
import json
import pandas as pd                       
from urllib.parse import urljoin        

headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'), 
}
def spellchecker(comment_list):
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
            response_dict = json.loads(response)

            result_text = response_dict['message']['result']['html']
            result_text = re.sub(r'<\/?.*?>','',result_text)
            comment_list[comment_key]['cor_comment'] = result_text
        else:
            comment_list[comment_key]['cor_comment'] = comment
   
    return comment_list

if __name__ == '__main__':
    line = "저여자 뭐임."
    print("수정결과 : " + spellchecker(line))




