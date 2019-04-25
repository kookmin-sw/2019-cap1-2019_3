import pandas as pd
import time 
import re
from bs4 import BeautifulSoup
import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./chromedriver') 

def getCmt(url): 
	youtube_url = url 
	#유튜브 주소 
	driver.get(youtube_url) 
	body = driver.find_element_by_tag_name("body") 
	print('시작') 

	num_of_pagedowns = 7 
	datetime.date.today()

	while num_of_pagedowns: 
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(1) 
		num_of_pagedowns -= 1 

	#10번만 반복 (스크롤 횟수 설정 필요) 
	num_of_pagedowns = 30 
	while True: 
		body.send_keys(Keys.PAGE_DOWN) 
		time.sleep(1) 
		num_of_pagedowns -= 1 

		html = driver.page_source 
		result = BeautifulSoup(html,'html.parser') 
		body2 = result.find("body") 

		#영상 제목
		title = body2.find_all('yt-formatted-string', attrs={'class':'style-scope ytd-video-primary-info-renderer'}) 
		title1=title[0].get_text() 
		title1 = re.sub(r'[/\:*?<>"|!]',' ',title1) 

		thread=body2.find_all('ytd-comment-renderer', attrs={'class':'style-scope ytd-comment-thread-renderer'}) 
		last = body2.find('yt-formatted-string', attrs={'class':'count-text style-scope ytd-comments-header-renderer'}) 
		last = last.string 

		#총 댓글수
		last_t = re.sub('[^\d]','',last) 
		last_t = int(last_t) 

		#덧글수
		plus_c = 0
		plus_cmt = body2.find_all('span',attrs={'id':'more-text'}) 

		for count in plus_cmt: 
			count = count.get_text().strip() 
			if count == '답글 보기': 
				plus_c += 1 
			else: 
				cmts = re.sub('[^\d]','',count)
				plus_c += int(cmts)

		cmtlist=[]
		aulist = []
		for items in thread: 
			#댓글 내용 
			comments = items.find_all('yt-formatted-string', attrs={'id':'content-text'}) 
			#print(comments)
			#기간(시점) 
			peirod = items.select('yt-formatted-string > a')[0].get_text() 
			#글쓴이
			author = items.find_all('a',attrs={'id':'author-text'})

			for c in comments: 
				if c != None: 
					try: 
						cmt = c.string 
						if cmt == None:
							cmt = c.a.string
						cmt.replace("\ufeff","")
						cmtlist.append(cmt)
					except TypeError as e: 
						pass 
				else: 
					pass 

			for c in author: 
				if c != None: 
					try: 
						cmt = c.span.string 
						cmt = cmt.strip()
						aulist.append(cmt) 
					except TypeError as e: 
						pass 

				else: 
					pass 

		num_c = (len(cmtlist) + plus_c ) 
		print("total:",num_c) 
		if num_c >= last_t or num_c >= 150000: 
			break  
	print("cmt:",len(cmtlist)) 
	print("auth:",len(aulist)) 

	print('-'*50) 
	raw_data = {'comments':cmtlist,'author':aulist}
	result = pd.DataFrame(raw_data)

	#csv파일 저장 폴더 생성, 파일 저장 
	dir_path = './' 
	dir_name = 'comment' 
	if not os.path.isdir(dir_path+'/'+ dir_name + '/'): 
		os.mkdir(dir_path+'/'+ dir_name + '/') 

	try : 
		result.to_csv(dir_path+'/'+dir_name+'/'+title1+'.csv', encoding='utf-8') 
	except Exception as e: 
		print(e, "저장 오류 발생")


url = input("url을 입력하세요 : ")
getCmt(url)

