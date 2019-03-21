from ImgLoader import ImgLoader
from Receiver import Receiver

class Sender:
    def __init__(self):
        self.imgLoader = ImgLoader()
        self.receiver = Receiver()
        pass

    def registVideo(self, path):
        pass

    def getThisFrame(self):
        #when it called, send 1 img and get 1 img 
        #rec.passProcessing(this_img)#하나 넘기고, 결과 받음
        pass

    def next(self):
        pass

 