import cv2

from subprocess import call

import os
import numpy as np
import json

from Oracle import Oracle
from Tensor_Mini_Xception import Tensor_Mini_Xception as TMX
from ImgLoader import ImgLoader




def search(dirname):
    filenames = os.listdir(dirname)
    result = []
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)#dirname + '/' + filename #
        result.append(full_filename)
    return result

def make_relative_to_absolute(R_path):
    result = os.path.dirname( os.path.abspath( __file__ ) )
    my_dirs = R_path.split('/')
    for each in my_dirs:
        if each == '.':
            continue
        result = os.path.join(result, each)
        #print('mid term check', result)

    return result
def downloadYouTube(videourl, path):
    current_path = os.path.dirname( os.path.abspath( __file__ ) )
    download_path = os.path.abspath(os.path.join(current_path, 'videos'))

    video_url = videourl

    serial = video_url.split('v=')[1]

    download_path = os.path.abspath(os.path.join(download_path, serial))

    os.mkdir(download_path)

    download_path += '/%(title)s.%(ext)s'

    print(download_path)
    command = "youtube-dl -f 133 -o "+ download_path + " --no-check-certificate " + videourl
    call(command.split(), shell=False)



def downloadYouTube_if_not_exist(video_url, download_path, serial):
    my_download_path = make_relative_to_absolute(download_path)
    my_video_path = make_relative_to_absolute(download_path+'/'+serial)

    video_list = search(my_download_path)

    exist = False
    for each in video_list:
        if each == my_video_path:#serial:
            exist = True
    if exist == False:
        print("There's no video with this name. Download start.")
        downloadYouTube(video_url, my_video_path)
    else:
        print("Video already exist. Loading start")

    video_list = search(my_video_path)

    return video_list[0]#return video name

class Commander:
    def __init__(self):
        model_path = './models/_mini_XCEPTION.61-0.65.hdf5'
        face_detect_model = './haarcascade_files/FaceDetect/haarcascade_frontalface_default.xml'
        self.oracle = TMX(model_path, face_detect_model)#Oracle: 
        self.imgLoader = ImgLoader()

    def for_web_cam(self, use_i_th_frame, file_path):
        #registing
        print("start registing")
        self.imgLoader.registVideo( file_path )

        #process (use loop)
        emotion_list = []
        i=0
        print("start extracting")
        faces = []
        drow_this_faces = []
        preds = [[0, 0, 0, 0, 0 ,0 ,0]]
        drow_this_preds = [[]]

        capture = []
        cur_faces_len = 0
        count =0
        while(self.imgLoader.isOpened()):
            i+=1

            if i%500 == 0:
                print(i,'th frame is proceed.')

            img = self.imgLoader.getThisFrame()

            if img is None:
                print('img == None')
                break

            if i%use_i_th_frame==0:#per i th frame
                 #preds = [[0, 0, 0, 0, 0 ,0 ,0]]
                 preds, faces = self.oracle.predict_and_return_others(img)

                 pred_array = np.array(preds)
                 pred_array = np.transpose(pred_array)
                 pred_emotion_average_list = [np.average(each) for each in pred_array]
                 pred_array = np.transpose(pred_emotion_average_list)

                 if len(pred_array) != 0:
                     emotion_list.append(pred_array)
                     drow_this_faces = faces
                     drow_this_preds = preds

                 if count<5:
                     #print('test here count ', count)
                     for (fX,fY,fW,fH) in faces:
                         capture = img[fY:fY + fH, fX:fX + fW]#cut face image
                         count +=1
                         break
                         


            #if len(faces) != 0:
            #self.oracle.just_drow(img, drow_this_faces, drow_this_preds)

        #    cv2.imshow("image", img)
        #    cv2.waitKey(35)#pause for 0.010 second 1000:1s = 1000/30=0.33 : 1f
        #cv2.destroyAllWindows()
            
        #print('start making json')
        emotion_array = np.array(emotion_list)

        emotion_array = np.transpose(emotion_array)

        emotion_average_list = [np.average(each) for each in emotion_array]

        EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
        emotion_dict_list = []#dict()
        emotion_dict = dict()
        for j in range(len(emotion_average_list)):#(7):
            emotion_dict[ EMOTIONS[j] ] = emotion_average_list[j]
            emotion_dict_list.append( { "label":EMOTIONS[j], "value":emotion_average_list[j] } )

        dumped = json.dumps(str(emotion_dict_list))[1:-1]
        dumped = dumped.replace("'", '"')

        self.imgLoader.release()

        return dumped , capture


    def for_youtube_video_piechart(self, use_i_th_frame, video_url):
        #download
        serial = video_url.split('v=')[1]
        download_path = './videos'
        print('download path : ', download_path)

        video_name = downloadYouTube_if_not_exist(video_url, download_path, serial)
        print(video_name)

        #registing
        print("start registing")
        self.imgLoader.registVideo(video_name)

        #process (use loop)
        emotion_list = []
        i=0
        print("start extracting")
        faces = []
        while(self.imgLoader.isOpened()):
            i+=1

            if i%500 == 0:
                print(i,'th frame is proceed.')

            img = self.imgLoader.getThisFrame()

            if img is None:
                print('img == None')
                break

            if i%use_i_th_frame==0:#per i th frame
                 preds = [[0, 0, 0, 0, 0 ,0 ,0]]
                 preds, faces = self.oracle.predict_and_return_others(img)


                 pred_array = np.array(preds)
                 pred_array = np.transpose(pred_array)
                 pred_emotion_average_list = [np.average(each) for each in pred_array]
                 pred_array = np.transpose(pred_emotion_average_list)

                 if len(pred_array) != 0:
                     emotion_list.append(pred_array)
            
        #print('start making json')
        emotion_array = np.array(emotion_list)

        emotion_array = np.transpose(emotion_array)

        emotion_average_list = [np.average(each) for each in emotion_array]

        EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
        emotion_dict_list = []#dict()
        emotion_dict = dict()
        for j in range(len(emotion_average_list)):#(7):
            emotion_dict[ EMOTIONS[j] ] = emotion_average_list[j]
            emotion_dict_list.append( { "label":EMOTIONS[j], "value":emotion_average_list[j] } )

        dumped = json.dumps(str(emotion_dict_list))[1:-1]
        dumped = dumped.replace("'", '"')
        return dumped


    def for_youtube_video_TimeLine(self, use_i_th_frame, video_url):
        #download
        serial = video_url.split('v=')[1]
        download_path = './videos'
        print('download path : ', download_path)

        video_name = downloadYouTube_if_not_exist(video_url, download_path, serial)
        print(video_name)

        #registing
        print("start registing")
        self.imgLoader.registVideo(video_name)

        #process (use loop)
        emotion_list = []
        face_list = []
        i_list=[]
        i=0
        print("start extracting")
        faces = []
        while(self.imgLoader.isOpened()):
            i+=1

            if i%500 == 0:
                print(i,'th frame is proceed.')

            img = self.imgLoader.getThisFrame()

            if img is None:
                print('img == None')
                break

            if i%use_i_th_frame==0:#per i th frame
                 preds = [[0, 0, 0, 0, 0 ,0 ,0]]
                 preds, faces = self.oracle.predict_and_return_others(img)

                 pred_array = np.array(preds)
                 pred_array = np.transpose(pred_array)
                 pred_emotion_average_list = [np.average(each) for each in pred_array]
                 pred_array = np.transpose(pred_emotion_average_list)

                 if len(pred_array) != 0:
                     emotion_list.append(pred_array)
                     for (fX,fY,fW,fH) in faces:#add face picture
                         roi = img[fY:fY + fH, fX:fX + fW]#cut face image
                         break
                     face_list.append(roi)

                     i_list.append(i)

        #print('start making json')
        emotion_array = np.array(emotion_list)

        emotion_array = np.transpose(emotion_array)

        emotion_average_list = [np.average(each) for each in emotion_array]

        EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
        emotion_dict_list = []#dict()
        emotion_dict = dict()
        for j in range(len(emotion_average_list)):#(7):
            emotion_dict[ EMOTIONS[j] ] = emotion_average_list[j]
            emotion_dict_list.append( { "label":EMOTIONS[j], "value":emotion_average_list[j] } )

        dumped = json.dumps(str(emotion_dict_list))[1:-1]
        dumped = dumped.replace("'", '"')

        max_emotion_list = [ EMOTIONS[np.argmax(each)] for each in np.transpose(emotion_array)]

        '''#use this code if you want to see the faces
        for each in face_list:
            cv2.imshow("image", each)
            cv2.waitKey(300)#pause for 0.010 second 1000:1s = 1000/30=0.33 : 1f
        cv2.destroyAllWindows()
        '''

        return dumped, max_emotion_list, i_list, face_list


