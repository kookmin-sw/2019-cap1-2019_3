import cv2
from pytube import YouTube
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
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)


def downloadYouTube_if_not_exist(video_url, download_path, serial):
    my_download_path = download_path
    my_video_path = download_path+'/'+serial

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

    def mainLogic(self, video_url):
        #downloading
        serial = video_url.split('v=')[1]
        download_path = './videos'
        print('download path : ', download_path)
        video_name = downloadYouTube_if_not_exist(video_url, download_path, serial)
        print(video_name)

        #registing
        print("start registing")
        self.imgLoader.registVideo(video_name)
        print("Video opened at server(Commender).")

        #process (use loop)
        emotion_list = []
        i=0
        print("start extracting")
        faces = []
        while(self.imgLoader.isOpened()):
            i+=1
            if i > 3002 :
                break
            if i %1000==1:
                print( i//30,'second')

            img = self.imgLoader.getThisFrame()

            if img is None:
                print('img == None')
                break

            if i % 30 == 1 : #1frame per 1 second.#True:##i>2500 and i%2 ==1:
                 preds = [0, 0, 0, 0, 0 ,0 ,0]
                 preds, faces = self.oracle.predict_and_return_others(img)
                 for each in preds:
                     emotion_list.append(each)
                 print(np.array(emotion_list).shape)

            if len(faces) != 0:
                self.oracle.just_drow(img, faces, preds)#must divide this into class

            cv2.imshow("image", img)
            cv2.waitKey(15)#pause for 0.010 second 1000:1s = 1000/30=0.33 : 1f

        emotion_array = np.array(emotion_list)
        print(emotion_array.shape)
        emotion_array = np.transpose(emotion_array)
        print(emotion_array.shape)
        emotion_average_list = [np.average(each) for each in emotion_array]
        print(len(emotion_average_list))
        print(np.array(emotion_average_list).shape)

        EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
        emotion_dict_list = []
        emotion_dict = dict()
        for j in range(len(emotion_average_list)):
            emotion_dict[ EMOTIONS[j] ] = emotion_average_list[j]
            emotion_dict_list.append( { "label":EMOTIONS[j], "value":emotion_average_list[j] } )

        print(emotion_dict_list)
        print('#############')
        with open('video_data.json', 'w') as f:
            dumped = json.dumps(str(emotion_dict_list))[1:-1]
            dumped = dumped.replace("'", '"')
            f.write( dumped )

        print('finished')
        cv2.destroyAllWindows()

        return emotion_list





