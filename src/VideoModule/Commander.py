import cv2

from Oracle import Oracle
from Tensor_Mini_Xception import Tensor_Mini_Xception as TMX

class Commander:
    def __init__(self):
        model_path = './models/_mini_XCEPTION.61-0.65.hdf5'
        face_detect_model = './haarcascade_files/FaceDetect/haarcascade_frontalface_default.xml'
        self.oracle = TMX(model_path, face_detect_model)

    def mainLogic(self, img):
        if img is not None:
            emotions = self.oracle.predict(img)
            print(emotions)
        else:
            print("Img has not been received")






