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
            vid = str(v.id)
            return redirect(vid+'/detail')

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

		key = 'AIzaSyD5EuiUIl4UGa1uKt0yb1IGfUNWtISbIog'

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

		key = 'AIzaSyD5EuiUIl4UGa1uKt0yb1IGfUNWtISbIog'

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
