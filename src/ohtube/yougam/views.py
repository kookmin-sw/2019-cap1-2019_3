from django.shortcuts import render ,get_object_or_404,redirect
from django.http import HttpResponse
import sys

# Create your views here.
from .models import Comment
from .models import Video
from .forms import PostForm
from .models import ReplyData

import os
import datetime, dateutil.parser

def change(request,video,cid,senti):
	if(senti=="0"):
		cmt = Comment.objects.get(video=video,cid=cid)
		cmt.label = 0
		cmt.save()
		comments = Comment.objects.filter(video=video)
		return render(request,"yougam/default.html",{"cmts":comments})
	elif(senti=="1"):
		cmt = Comment.objects.get(video=video,cid=cid)
		cmt.label = 1
		cmt.save()
		comments = Comment.objects.filter(video=video)
		return render(request,"yougam/default.html",{"cmts":comments})
	else:
		cmt = Comment.objects.get(video=video,cid=cid)
		cmt.label = 2
		cmt.save()
		comments = Comment.objects.filter(video=video)
		return render(request,"yougam/default.html",{"cmts":comments})

def post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            video = form.save(commit = False)
            cnt = Video.objects.filter(url=video.url).count()
            #이미 분석한 video
            if(cnt > 0):
                pass
            #새로운 비디오
            else:
                video.generate()
            v = Video.objects.get(url=video.url)
            vid = v.id
            return redirect('detail', video = vid)

        else:
            return HttpResponse("not valid url!")
    else:
        form = PostForm()
        return render(request, "yougam/index.html",{"form": form})

def creator(request,video):
	vid = Video.objects.get(id=video)
	if Comment.objects.filter(video=vid).count() < 1:
		module_path=os.path.join(os.path.dirname(os.path.abspath( __file__ ) ), 'code')
		sys.path.append(module_path)
		temp = Video.objects.get(id=video)
		url = temp.url

		import predict
		from youtube_api_cmd import YouTubeApi
		import spellcheck

		key = ''

		y = YouTubeApi(100,url,key)
		dic = {}
		label = {}
		comments = {}
		dic = y.get_video_comment()
		print("댓글 수집 완료")
		comments = spellcheck.spellchecker(dic)
		print("맞춤법 수정 완료")
		label = predict.labeling(comments)
		print("라벨링 완료")
		for i in range(1,len(dic)+1):
			vid = Video.objects.get(id=video)
			d = dateutil.parser.parse(dic[i]["period"])
			d = d.strftime('%Y/%m/%d')
			c = Comment(video=vid,cid=i,cmt=dic[i]['comment'],label=label[i],author=dic[i]["author"],period=d,like=dic[i]["like"])
			c.generate()

	#이미 분석한것은 보여주기만 하면됨
	else:
		pass
	comments = Comment.objects.filter(video=video)

	vid = Video.objects.get(id=video)
	no1 = Comment.objects.filter(video=vid).order_by('-like')[0]
	no2 = Comment.objects.filter(video=vid).order_by('-like')[1]
	no3 = Comment.objects.filter(video=vid).order_by('-like')[2]


	return render(request,"yougam/cre.html",{"no1":{no1.cmt,no1.label},"no2":{no2.cmt,no2.label}
		,"no3":{no3.cmt,no3.label}})

def detail(request,video):
	#새로운 비디오는 predict 해야함
	if Comment.objects.filter(video=video).count() < 1:
		module_path=os.path.join(os.path.dirname(os.path.abspath( __file__ ) ), 'code')
		sys.path.append(module_path)
		temp = Video.objects.get(id=video)
		url = temp.url

		import predict
		from youtube_api_cmd import YouTubeApi
		import spellcheck

		key = ''

		y = YouTubeApi(100,url,key)
		dic = {}
		label = {}
		comments = {}
		dic = y.get_video_comment()
		print("댓글 수집 완료")
		comments = spellcheck.spellchecker(dic)
		print("맞춤법 수정 완료")
		label = predict.labeling(comments)
		print("라벨링 완료")
		for i in range(1,len(dic)+1):
			vid = Video.objects.get(id=video)
			d = dateutil.parser.parse(dic[i]["period"])
			d = d.strftime('%Y/%m/%d')
			c = Comment(video=vid,cid=i,cmt=dic[i]['comment'],label=label[i],author=dic[i]["author"],period=d,like=dic[i]["like"])
			c.generate()


			# if 'replies' in dic[i]:
			# 	for j in range(1,len(dic[i]['replies'])+1):
			# 		d = dateutil.parser.parse(dic[i]["replies"][j]['period'])
			# 		d = d.strftime('%Y/%m/%d')
			# 		cid = Comment.objects.get(cid=i)
			# 		c = ReplyData(parent_id=cid,comment=dic[i]['replies'][j]['comment'],author=dic[i]['replies'][j]['author'],period=d)
			# 		c.generate()

	#이미 분석한것은 보여주기만 하면됨
	else:
		pass
	comments = Comment.objects.filter(video=video)
	return render(request,"yougam/default.html",{"cmts":comments})

def user(request):
	return render(request,"yougam/user.html")
















from django.http import HttpResponse
from .models import Comment, Video
from .forms import PostForm
from django.shortcuts import render, redirect
import json
import sys
import os
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen

YOUTUBE_API_KEY = ''

def first_show(request, video):

    video_url = Video.objects.get(pk=video)

    comment_module_path=os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'code/crawler')
    sys.path.append(comment_module_path)
    from youtube_api_cmd import YouTubeApi

    comment_obj = YouTubeApi(100,video_url.url,YOUTUBE_API_KEY)
    comment_list = comment_obj.get_video_comment()
    print("--crawling complete--")
     #------crawling----------

    comment_module_path2=os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'code/predict_sentiment6')
    sys.path.append(comment_module_path2)
    import sentiment_count


    predicted_comment_list = sentiment_count.csvToDict(comment_list)
    predict_replies_list = {}
    reply_idx = 1

    for comment_info in predicted_comment_list:
        comment_text = predicted_comment_list[comment_info]['comment']
        comment_author = predicted_comment_list[comment_info]['author']
        comment_period = predicted_comment_list[comment_info]['period']
        comment_like = predicted_comment_list[comment_info]['like']
        comment_label = predicted_comment_list[comment_info]['label']
        parent_comment = video_url.comment_set.create(video = video, cmt = comment_text, label6 = comment_label, author = comment_author, period = comment_period, like = comment_like)
        # print(predicted_comment_list[comment_info])

        if 'replies' in predicted_comment_list[comment_info].keys():
            replies_list = predicted_comment_list[comment_info]['replies']
            predicted_replies_list = sentiment_count.csvToDict(replies_list)
            parent_id = parent_comment.id
            for reply_info in predicted_replies_list:
                reply_text = predicted_replies_list[reply_info]["comment"]
                reply_author = predicted_replies_list[reply_info]["author"]
                reply_period = predicted_replies_list[reply_info]["period"]
                reply_like = predicted_replies_list[reply_info]["like"]
                reply_label = predicted_replies_list[reply_info]["label"]
                predict_replies_list[reply_idx] = {'comment': reply_text, 'author': reply_author, 'label' : reply_label}
                parent_comment.replydata_set.create(parent_id = parent_id, comment = reply_text, label6 = reply_label, author = reply_author, period = reply_period, like = reply_like)
                reply_idx += 1

        print("--predict complete--")
    predict_count_cmt = sentiment_count.sentenceCount(predicted_comment_list)
    predict_count_reply = sentiment_count.sentenceCount(predict_replies_list)

    cmt_count_list = []
    reply_count_list = []
    count_list = []
    for senti in predict_count_cmt:
        cmt_count_list.append(predict_count_cmt[senti])
    for senti in predict_count_reply:
        reply_count_list.append(predict_count_reply[senti])

    for i in range(0,6):
        count_list.append(cmt_count_list[i] + reply_count_list[i])
        print(count_list[i])
    video_url.sentiment_neutral = count_list[0]
    video_url.sentiment_happy = count_list[1]
    video_url.sentiment_sad = count_list[2]
    video_url.sentiment_surprise = count_list[3]
    video_url.sentiment_anger = count_list[4]
    video_url.sentiment_fear = count_list[5]
    video_url.generate()
    return render(request, 'input_url.html', {"count": count_list})


def show(request, video):
	video_url = Video.objects.get(pk=video)
	loaded_count_list = []
	loaded_count_list.append(video_url.sentiment_neutral)
	loaded_count_list.append(video_url.sentiment_happy)
	loaded_count_list.append(video_url.sentiment_sad)
	loaded_count_list.append(video_url.sentiment_surprise)
	loaded_count_list.append(video_url.sentiment_anger)
	loaded_count_list.append(video_url.sentiment_fear)
	print(loaded_count_list)
	return render(request, 'input_url.html', {"count": loaded_count_list})

def typeRecieve(request):

    if 'user' in request.POST:
        return render(request, 'input_url.html', {"chosenType": 1})

    elif 'creator' in request.POST:
        return render(request, 'input_url.html', {"chosenType": 2})

    else:
        return render(request, 'input_url.html')

def post6(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			video_url = form.save(commit = False)
			if Video.objects.filter(url=video_url.url).count() == 1:
				video_url = Video.objects.get(url=video_url.url)
				print(1)
				return redirect('shows', video = video_url.id)
			elif Video.objects.filter(url=video_url.url).count() == 0:
				video_url.generate()
				return redirect('first_show', video = video_url.id)
	else:
		form = PostForm()
		return render(request, 'input_url.html', {"form": form})
