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

        if(len(cmt)) < 500:
            url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy?'
            params = {}
            params['_callback'] = 'jQuery112409312646700220539_1557421638284'
            params['q'] = cmt
            params['where'] = "nexearch"
            params['color_blindness'] = 0
            params['_'] = 1557292527466

            response = requests.get(url,params=params).text
            response = response.replace(params['_callback'] + '(','')
            response = response.replace(');','')
            response_dict = json.loads(response)

            result_text = response_dict['message']['result']['html']
            result_text = re.sub(r'<\/?.*?>','',result_text)
            result[i] = result_text
        else:
            result[i] = cmt

        # if 'replies' in dic[i]:

        #     for j in range(1,len(dic[i]['replies'])+1):
        #         cmt = dic[i]['replies'][j]['comment'].replace('\ufeff','').replace('\ud80c','')

        #         if(len(cmt)) < 500:
        #             url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy?'
        #             params = {}
        #             params['_callback'] = 'jQuery112409312646700220539_1557421638284'
        #             params['q'] = cmt
        #             params['where'] = "nexearch"
        #             params['color_blindness'] = 0
        #             params['_'] = 1557292527466

        #             response = requests.get(url,params=params).text
        #             response = response.replace(params['_callback'] + '(','')
        #             response = response.replace(');','')
        #             response_dict = json.loads(response)

        #             result_text = response_dict['message']['result']['html']
        #             result_text = re.sub(r'<\/?.*?>','',result_text)
        #             if(j==1):
        #                 result[i] = {1:result_text}
        #             else:
        #                 result[i][j] = result_text
        #         else:
        #             if(j==1):
        #                 result[i] = {1:cmt}
        #             else:
        #                 result[i][j] = cmt

    return result

if __name__ == '__main__':
    line = "저여자 뭐임."
    print("수정결과 : " + spellchecker(line))




