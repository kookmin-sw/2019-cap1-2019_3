from django.shortcuts import render ,get_object_or_404,redirect
from django.http import HttpResponse
import sys
import json #add 0516

# Create your views here.
from .models import Comment
from .models import Video
from .forms import PostForm
from .models import ReplyData
from .models import TimeLog
from .models import PieChart
from .models import WebCam

from django.utils.safestring import SafeString

import os
import datetime, dateutil.parser

def change(request,video,cid,senti):

   video_urls = Video.objects.get(pk=video)
   temp_url = video_urls.url
   iframe_url = temp_url.replace('https://www.youtube.com/watch?v=','https://www.youtube.com/embed/')

   loaded_count_list = []
   loaded_count_list.append(video_urls.sentiment_neutral)
   loaded_count_list.append(video_urls.sentiment_happy)
   loaded_count_list.append(video_urls.sentiment_sad)
   loaded_count_list.append(video_urls.sentiment_surprise)
   loaded_count_list.append(video_urls.sentiment_anger)
   loaded_count_list.append(video_urls.sentiment_fear)
   print(loaded_count_list)

   video_title = video_urls.title
   reply = ReplyData.objects.filter(video=video)

   video_id = video
   video_instance = Video.objects.get(pk=video_id)
   video_url = video_instance.url
   logs = TimeLog.objects.filter(url=video_url)
   poll_results = PieChart.objects.get(video_id=video_id)

   if(senti=="0"):
      cmt = Comment.objects.get(video=video,cid=cid)
      cmt.label = 0
      cmt.save()
      comments = Comment.objects.filter(video=video)
      return render(request, "yougam/user.html", {"count":loaded_count_list,"cmts":comments,"iframe_url":iframe_url, "video_id": video_urls.id,"logs":logs,"json": SafeString(poll_results.json_data),"video_title":video_title,"reply":reply})
   elif(senti=="1"):
      cmt = Comment.objects.get(video=video,cid=cid)
      cmt.label = 1
      cmt.save()
      comments = Comment.objects.filter(video=video)
      return render(request, "yougam/user.html", {"count":loaded_count_list,"cmts":comments,"iframe_url":iframe_url, "video_id": video_urls.id,"logs":logs,"json": SafeString(poll_results.json_data),"video_title":video_title,"reply":reply})
   else:
      cmt = Comment.objects.get(video=video,cid=cid)
      cmt.label = 2
      cmt.save()
      comments = Comment.objects.filter(video=video)
      return render(request, "yougam/user.html", {"count":loaded_count_list,"cmts":comments,"iframe_url":iframe_url, "video_id": video_urls.id,"logs":logs,"json": SafeString(poll_results.json_data),"video_title":video_title,"reply":reply})

def post(request):
   if request.method == "POST":
      form = PostForm(request.POST)

      if form.is_valid():
         video = form.save(commit = False)
         cnt = Video.objects.filter(url=video.url).count()

         if cnt == 0 :
            video.generate()

         v = Video.objects.get(url=video.url)
         vid = v.id
      else : return HttpResponse("not valid url!")
   else:
      form = PostForm()
      return render(request, "yougam/index.html",{"form": form})


   value = request.POST.get('typeRadio')

   if 'user' == value :
      return redirect('userdetail', video = vid)

   elif 'creator' == value :
      return redirect('crtdetail', video = vid)

   else : return HttpResponse("type is empty!")


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


def userdetail(request, video):

   video_url = Video.objects.get(pk=video)
   temp_url = video_url.url
   iframe_url = temp_url.replace('https://www.youtube.com/watch?v=','https://www.youtube.com/embed/')

   if Comment.objects.filter(video=video_url.id).count() < 1:
      comment_module_path=os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'code/crawler')
      sys.path.append(comment_module_path)

      module_path=os.path.join(os.path.dirname(os.path.abspath( __file__ ) ), 'code/predict_sentiment')
      sys.path.append(module_path)

      comment_module_path2=os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'code/predict_sentiment6')
      sys.path.append(comment_module_path2)

      with open("yougam/static/api_key/youtube_api.txt", "r") as y_api :
         YOUTUBE_API_KEY = y_api.readline()

      from youtube_api_cmd import YouTubeApi
      import sentiment_count
      import predict
      import spellcheck
      import random

      import sentiment_wordcloud

      comment_obj = YouTubeApi(100,video_url.url,YOUTUBE_API_KEY)

      comment_list = comment_obj.get_video_comment()
      video_title  = comment_obj.get_video_title()
      video_url.title = video_title
      video_url.generate()
      print(video_title)
      print("--comment collect complete--")

      comments = spellcheck.spellchecker(comment_list)
      print("--comment spellcheck complete--")

      label = predict.labeling(comments)
      print("--comment positibe/negative complete--")

       #------crawling----------

      predicted_comment_list = sentiment_count.predict_senti6(comment_list)
      predict_replies_list = {}
      reply_idx = 1

      for comment_info in predicted_comment_list:
         comment_text = predicted_comment_list[comment_info]['comment']
         comment_author = predicted_comment_list[comment_info]['author']
         comment_period = predicted_comment_list[comment_info]['period']
         comment_like = predicted_comment_list[comment_info]['like']
         comment_label = predicted_comment_list[comment_info]['label']
         comment_labelpn = label[comment_info]['label_pn']
         parsed_date = dateutil.parser.parse(comment_period)
         parsed_date = parsed_date.strftime('%Y/%m/%d')
         ran = random.randint(1,9)
         parent_comment = video_url.comment_set.create(video = video, cid=comment_info,cmt = comment_text,label= comment_labelpn,label6 = comment_label, author = comment_author, period = parsed_date, like = comment_like,randnum=ran)
         # print(predicted_comment_list[comment_info])

         if 'replies' in predicted_comment_list[comment_info].keys():
            replies_list = predicted_comment_list[comment_info]['replies']
            replies_list2 = label[comment_info]['replies']
            # predicted_replies_list = sentiment_count.predict_senti6(replies_list)
            predicted_replies_list2 = spellcheck.spellchecker(replies_list2)
            predicted_replies_list2 = predict.labeling(predicted_replies_list2)

            parent_id = parent_comment.id
            for reply_info in replies_list:
               predict_replies_list[reply_idx] = replies_list[reply_info]
               reply_text = replies_list[reply_info]["comment"]
               reply_author = replies_list[reply_info]["author"]
               reply_period = replies_list[reply_info]["period"]
               reply_like = replies_list[reply_info]["like"]
               # reply_label = replies_list[reply_info]["label"]
               reply_labelpn = replies_list[reply_info]["label_pn"]
               parsed_date = dateutil.parser.parse(reply_period)
               parsed_date = parsed_date.strftime('%Y/%m/%d')
               this_reply = parent_comment.replydata_set.create(video = video,pid=comment_info, parent_id = parent_id, comment = reply_text, label = reply_labelpn, author = reply_author, period = parsed_date, like = reply_like)
               predict_replies_list[reply_idx]["rid"] = this_reply.id
               reply_idx += 1

      predicted_replies_list = sentiment_count.predict_senti6(predict_replies_list)
      for i in predicted_replies_list:
          find_id = predicted_replies_list[i]["rid"]
          found_reply = ReplyData.objects.get(id=find_id)
          found_reply.label6 = predicted_replies_list[i]["label"]
          found_reply.generate()
      print("--comment6 predict complete--")

      predict_count_cmt = sentiment_count.sentenceCount(predicted_comment_list)
      predict_count_reply = sentiment_count.sentenceCount(predicted_replies_list)
      sentiment_wordcloud.wordcloud(predicted_comment_list, predicted_replies_list, video_url.id)

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

   video_url = Video.objects.get(pk=video_url.id)
   loaded_count_list = []
   loaded_count_list.append(video_url.sentiment_neutral)
   loaded_count_list.append(video_url.sentiment_happy)
   loaded_count_list.append(video_url.sentiment_sad)
   loaded_count_list.append(video_url.sentiment_surprise)
   loaded_count_list.append(video_url.sentiment_anger)
   loaded_count_list.append(video_url.sentiment_fear)
   print(loaded_count_list)

   comments = Comment.objects.filter(video=video)
   reply = ReplyData.objects.filter(video=video)
   temp_url = video_url.url
   video_title = video_url.title
   iframe_url = temp_url.replace('https://www.youtube.com/watch?v=','https://www.youtube.com/embed/')
   vid = video_url.id
   print("comment predict complete!")
   print("video predict start!")



   from PIL import Image
   import cv2
   video_instance = Video.objects.get(pk=video)
   video_url = video_instance.url
   use_i_th_frame = 300 #30==1sec
   data = PieChart.objects.filter(video_id=video)#video_url) #url로 하고 싶으면 이걸 사용.
   if data.count() < 1:
      print("There are no data. start task")
      current_path = os.path.dirname( os.path.abspath( __file__ ) )
      code_path = os.path.abspath(os.path.join(current_path, 'code'))
      videoModule_path = os.path.abspath(os.path.join(code_path, 'VideoModule'))
      sys.path.append(videoModule_path)
      from Commander import Commander
      commander = Commander()
      dumped, max_emotion_list, i_list, face_list = commander.for_youtube_video_TimeLine(use_i_th_frame, video_url)
      will_inserted = PieChart(video_id = str(video), json_data = dumped)
      img_path_list = []
      for j in range(len(i_list)):
         fileName = str(video) + "_" + str(i_list[j]) + ".png"
         save_dir = os.path.abspath(os.path.join(current_path, os.pardir))
         save_dir = os.path.abspath(os.path.join(save_dir, 'media'))
         save_dir = os.path.abspath(os.path.join(save_dir, fileName))
         destRGB = cv2.cvtColor(face_list[j], cv2.COLOR_BGR2RGB)
         pic_file = Image.fromarray(destRGB, 'RGB')
         pic_file.save(save_dir)
         img_path_list.append( fileName )
      timeLog_list = []
      for j in range(len(i_list)):
         second = (i_list[j]//30)%60
         minute = ((i_list[j]//30)//60 )%60
         hour = ((i_list[j]//30)//60 )//60
         time_str = ""
         if hour<10:
             time_str += ('0' + str(hour))
         else:
             time_str += str(hour)
         time_str += ":"
         if minute<10:
             time_str += ('0' + str(minute))
         else:
             time_str += str(minute)
         time_str += ":"
         if second<10:
             time_str += ('0' + str(second))
         else:
             time_str += str(second)
         timeLog_list.append( TimeLog(top_sentiment = max_emotion_list[j], url = video_url, time = time_str, img_path = img_path_list[j]) )
      for j in range(len(i_list)):
         timeLog_list[j].save()
      will_inserted.save()
   else:
      print("data already exist")
      pass
   video_id = video
   video_instance = Video.objects.get(pk=video_id)
   video_url = video_instance.url
   logs = TimeLog.objects.filter(url=video_url)
   poll_results = PieChart.objects.get(video_id=video_id)

   return render(request, "yougam/user.html", {"count":loaded_count_list,"cmts":comments, "video_id":vid, "iframe_url":iframe_url,"logs": logs, "json" : SafeString(poll_results.json_data), "video_title":video_title,"reply":reply})



def crtdetail(request, video):

   video_url = Video.objects.get(pk=video)


   if Comment.objects.filter(video=video_url.id).count() < 1:
      comment_module_path=os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'code/crawler')
      sys.path.append(comment_module_path)

      module_path=os.path.join(os.path.dirname(os.path.abspath( __file__ ) ), 'code/predict_sentiment')
      sys.path.append(module_path)

      comment_module_path2=os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'code/predict_sentiment6')
      sys.path.append(comment_module_path2)

      with open("yougam/static/api_key/youtube_api.txt", "r") as y_api :
         YOUTUBE_API_KEY = y_api.readline()

      from youtube_api_cmd import YouTubeApi
      import sentiment_count
      import predict
      import spellcheck
      import random

      comment_obj = YouTubeApi(100,video_url.url,YOUTUBE_API_KEY)

      comment_list = comment_obj.get_video_comment()
      video_title  = comment_obj.get_video_title()

      print("--comment collect complete--")

      comments = spellcheck.spellchecker(comment_list)
      print("--comment spellcheck complete--")

      label = predict.labeling(comments)
      print("--comment positive/negative label complete--")

       #------crawling----------

      predicted_comment_list = sentiment_count.predict_senti6(comment_list)
      predict_replies_list = {}
      reply_idx = 1

      for comment_info in predicted_comment_list:
         comment_text = predicted_comment_list[comment_info]['comment']
         comment_author = predicted_comment_list[comment_info]['author']
         comment_period = predicted_comment_list[comment_info]['period']
         comment_like = predicted_comment_list[comment_info]['like']
         comment_label = predicted_comment_list[comment_info]['label']
         comment_labelpn = label[comment_info]['label_pn']
         parsed_date = dateutil.parser.parse(comment_period)
         parsed_date = parsed_date.strftime('%Y/%m/%d')
         ran = random.randint(1,9)
         parent_comment = video_url.comment_set.create(video = video, cid=comment_info,cmt = comment_text,label= comment_labelpn,label6 = comment_label, author = comment_author, period = parsed_date, like = comment_like,randnum=ran)
         # print(predicted_comment_list[comment_info])

         if 'replies' in predicted_comment_list[comment_info].keys():
            replies_list = predicted_comment_list[comment_info]['replies']
            replies_list2 = label[comment_info]['replies']
            # predicted_replies_list = sentiment_count.predict_senti6(replies_list)
            predicted_replies_list2 = spellcheck.spellchecker(replies_list2)
            predicted_replies_list2 = predict.labeling(predicted_replies_list2)

            parent_id = parent_comment.id
            for reply_info in replies_list:
               predict_replies_list[reply_idx] = replies_list[reply_info]
               reply_text = replies_list[reply_info]["comment"]
               reply_author = replies_list[reply_info]["author"]
               reply_period = replies_list[reply_info]["period"]
               reply_like = replies_list[reply_info]["like"]
               # reply_label = replies_list[reply_info]["label"]
               reply_labelpn = replies_list[reply_info]["label_pn"]
               parsed_date = dateutil.parser.parse(reply_period)
               parsed_date = parsed_date.strftime('%Y/%m/%d')
               this_reply = parent_comment.replydata_set.create(video = video,pid=comment_info, parent_id = parent_id, comment = reply_text, label = reply_labelpn, author = reply_author, period = parsed_date, like = reply_like)
               predict_replies_list[reply_idx]["rid"] = this_reply.id
               reply_idx += 1

      predicted_replies_list = sentiment_count.predict_senti6(predict_replies_list)
      for i in predicted_replies_list:
          find_id = predicted_replies_list[i]["rid"]
          found_reply = ReplyData.objects.get(id=find_id)
          found_reply.label6 = predicted_replies_list[i]["label"]
          found_reply.generate()
      print("--comment6 predict complete--")

      predict_count_cmt = sentiment_count.sentenceCount(predicted_comment_list)
      predict_count_reply = sentiment_count.sentenceCount(predicted_replies_list)

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

   vid = Video.objects.get(pk=video_url.id)
   loaded_count_list = []
   loaded_count_list.append(vid.sentiment_neutral)
   loaded_count_list.append(vid.sentiment_happy)
   loaded_count_list.append(vid.sentiment_sad)
   loaded_count_list.append(vid.sentiment_surprise)
   loaded_count_list.append(vid.sentiment_anger)
   loaded_count_list.append(vid.sentiment_fear)
   print(loaded_count_list)

   comments = Comment.objects.filter(video=video)
   video_title = vid.title
   no1 = Comment.objects.filter(video=vid).order_by('-like')[0]
   no2 = Comment.objects.filter(video=vid).order_by('-like')[1]
   no3 = Comment.objects.filter(video=vid).order_by('-like')[2]

   num_pos = Comment.objects.filter(video=vid).filter(label=2).count() + ReplyData.objects.filter(video=str(vid)).filter(label=2).count()
   num_net = Comment.objects.filter(video=vid).filter(label=1).count() + ReplyData.objects.filter(video=str(vid)).filter(label=1).count()
   num_neg = Comment.objects.filter(video=vid).filter(label=0).count() + ReplyData.objects.filter(video=str(vid)).filter(label=0).count()


   import numpy as np
   #take data
   if(WebCam.objects.filter(video_id=video).count() > 0):
      results = WebCam.objects.filter(video_id=video)
      print("@@@@@@@@@@@@@@@@")
      print(results[0].json_data)
      print("@@@@@@@@@@@@@@@@")
      emotion_list = [ each.json_data for each in results ]

      tmp=[]
      for i in range(len(emotion_list)):
         emotion_list[i] = emotion_list[i].replace('[' , '')
         emotion_list[i] = emotion_list[i].replace(']' , '')
         emotion_list[i] = emotion_list[i].replace('{' , '')
         emotion_list[i] = emotion_list[i].replace('}' , '')
         emotion_list[i] = emotion_list[i].replace(',' , '')
         tmp.append( emotion_list[i].split(' ') )
      print(emotion_list)
      emotion_list = []

      for each in tmp:
         tmp_list=[]
         for i in range(7):
            tmp_list.append( float(each[3+(4*i)]) )
         emotion_list.append(tmp_list)

      emotion_str = [ '"화남"',  '"혐오"',  '"놀람"',  '"행복"', '"슬픔"',  '"겁먹음"',  '"중립"',  ]

      if len(emotion_list) == 0:
         emotion_list = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

      #get average
      if len(emotion_list) >= 1:
         emotion_array = np.array(emotion_list)
         #print(emotion_array)
         emotion_array = np.transpose(emotion_array)
         #print(emotion_array)
         emotion_average_list = np.array([np.average(each) for each in emotion_array])
      else:
         emotion_average_list = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

      print(emotion_average_list)



      #back to json
      str_back = '[{label: "화남", value: %f},{label: "혐오", value: %f},{label: "놀람", value: %f},{label: "행복", value: %f},{label: "슬픔", value: %f},{label: "겁먹은", value: %f},{label: "중립", value: %f}]'%(emotion_average_list[0], emotion_average_list[1], emotion_average_list[2], emotion_average_list[3],emotion_average_list[4], emotion_average_list[5], emotion_average_list[6] )
      print(str_back)

      capture = WebCam.objects.filter(video_id=video)###time log랑똑같이 꺼냄####
      for each in capture:
          print(each)

   else:
      str_back = '[{label: "화남", value: %f},{label: "혐오", value: %f},{label: "놀람", value: %f},{label: "행복", value: %f},{label: "슬픔", value: %f},{label: "겁먹은", value: %f},{label: "중립", value: %f}]'%(0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0)

   video_id = video
   return render(request,"yougam/cre.html",{"no1":no1,"no2":no2,"no3":no3,"num_pos":num_pos,"num_neg":num_neg,"num_net":num_net, "video_title":video_title, "count":loaded_count_list,"json" : SafeString(str_back),"video_id":video_id})



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def sending(request): #웹캠 전달 받은 것 처리
    if request.method == 'POST':
        #경로설정
        current_path = os.path.dirname( os.path.abspath( __file__ ) )
        code_path = os.path.abspath(os.path.join(current_path, 'code'))
        videoModule_path = os.path.abspath(os.path.join(code_path, 'VideoModule'))
        sys.path.append(videoModule_path)

        # 폴더 하나 써서 추가하기: webcams
        current_url = request.POST.get('url')
        video = int(current_url.split('/')[-3])#seed1

        last_row = WebCam.objects.order_by('id').last()####
        last_row_id = 0
        if last_row is None:
            last_row_id = 0
        else:
            last_row_id = last_row.id

        file_path =str(video) +'_' + str(last_row_id+1)  +'.mp4'


        save_path = os.path.abspath(os.path.join(current_path, os.pardir))
        save_path = os.path.abspath(os.path.join(save_path, 'media'))
        save_path = os.path.abspath(os.path.join(save_path, file_path))

        with open(save_path, 'wb') as f:##경로 지정 하고, 이름 유니크하게 바꿔야.
            f.write(request.FILES['video'].read())

        #분석 및 저장
        use_i_th_frame = 9 #30==1sec

        from Commander import Commander
        import cv2
        from PIL import Image
        import numpy as np
        commander = Commander()
        dumped, capture = commander.for_web_cam(use_i_th_frame, save_path)

        capture_path =str(video) +'_' + str(last_row_id+1)  +'.png'


        capture_save_path = os.path.abspath(os.path.join(current_path, os.pardir))
        capture_save_path = os.path.abspath(os.path.join(capture_save_path, 'media'))
        capture_save_path = os.path.abspath(os.path.join(capture_save_path, capture_path))

        #print(capture_save_path)



        if len(dumped) != 0:
            destRGB = cv2.cvtColor(capture, cv2.COLOR_BGR2RGB)
            captured_img = Image.fromarray(destRGB, 'RGB')

            captured_img.save(capture_save_path)

            will_inserted = WebCam(video_id=str(video), json_data=dumped, video_path=save_path, capture_path=capture_save_path)
            will_inserted.save()

    else:
        return HttpResponse("Something Wrong in file uploading")

    context = {}
    return HttpResponse(json.dumps(context), "application/json")
