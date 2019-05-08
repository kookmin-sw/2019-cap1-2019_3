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

def spellchecker(dic):
    result = {}
    for i in range(1,len(dic)+1):
        cmt = dic[i]['comment'].replace('\ufeff','').replace('\ud80c','')
        url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy?'
        params = {}
        params['_callback'] = 'jQuery112409768473573854217_1557292527463'
        params['q'] = cmt
        params['where'] = "nexearch"
        params['color_blindness'] = 0
        params['_'] = 1557292527466

        response = requests.get(url,params=params).text
        #print(response)
        response = response.replace(params['_callback'] + '(','')
        #print(response)
        response = response.replace(');','')
        response_dict = json.loads(response)
        #print(response_dict)
        result_text = response_dict['message']['result']['html']
        result_text = re.sub(r'<\/?.*?>','',result_text)
        result[i] = result_text
    return result

if __name__ == '__main__':
    line = "저여자 뭐임."
    print("수정결과 : " + spellchecker(line))




