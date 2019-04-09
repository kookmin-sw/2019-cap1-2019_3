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
	#(스크롤 내리기) 
	num_of_pagedowns = 7 
	datetime.date.today()

	while num_of_pagedowns: 
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(2) 
		num_of_pagedowns -= 1 

		try: 
			driver.find_element_by_xpath('//*[@id="sort-menu"]').click() 
			#driver.find_element_by_xpath('//*[@id="menu"]/a[@tabindex="-1"]').click() 
			driver.find_element_by_xpath('//*[@id="menu"]/a[2]/paper-item/paper-item-body/div[text()="최근 날짜순"]').click() 
		except Exception as e: 
			pass 

	#10번만 반복 (스크롤 횟수 설정 필요) 
	num_of_pagedowns = 30 
	while True: 
		body.send_keys(Keys.PAGE_DOWN) 
		time.sleep(2) 
		num_of_pagedowns -= 1 

			# body = result.find("body") 
			# last = body.find_all('div', attrs={'id':'continuations'}) 
			# if last not in body: 
			# break 

		html = driver.page_source 
		result = BeautifulSoup(html,'html.parser') 
		#print(html) 
		body2 = result.find("body") 
		#print(body)

		title = body2.find_all('yt-formatted-string', attrs={'class':'style-scope ytd-video-primary-info-renderer'}) 
		title1=title[0].get_text() 
		title1 = re.sub(r'[/\:*?<>"|!]',' ',title1) 
		#print(title1) 
		thread=body2.find_all('ytd-comment-renderer', attrs={'class':'style-scope ytd-comment-thread-renderer'}) 
		last = body2.find('yt-formatted-string', attrs={'class':'count-text style-scope ytd-comments-header-renderer'}) 
		last = last.string 
		print(last)
		print(last) 
		
		last_t = re.sub('[^\d]','',last) 
		last_t = int(last_t) 
		plus_c = 0
		plus_cmt = body2.find_all('span',attrs={'id':'more-text'}) 

		for count in plus_cmt: 
			count = count.get_text().strip() 
			#print(count) 
			if count == '답글 보기': 
				plus_c += 1 
			else: 
				cmts = re.sub('[^\d]','',count)
				plus_c += int(cmts)

		#print(plus_c) 
		#print(last_t) 
		cmtlist=[]

		for items in thread: 
			#댓글 내용 
			div = items.find_all('yt-formatted-string', attrs={'id':'content-text'}) 
			#기간(시점) 
			div2 = items.select('yt-formatted-string > a')[0].get_text() 
			for lists in div: 
				#print(lists) 
				if lists != None: 
					try: 
						cmt = lists.string 
						#textcmt = re.sub(r"[^\w^?!',.%$]",' ',cmt) 
						cmtlist.append([cmt]) 
						#print(textcmt) 
					except TypeError as e: 
						pass 

				else: 
					pass 

			#cmtlist.append([textcmt, div2])
		num_c = (len(cmtlist) +plus_c ) 
		print(num_c) 
		if num_c >= (last_t-10) or num_c>=3500: 
			break 
			
	print(len(cmtlist)) 
	print('-'*50) 
	result = pd.DataFrame(cmtlist)

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

