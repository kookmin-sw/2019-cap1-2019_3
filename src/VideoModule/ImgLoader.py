import cv2


class ImgLoader:
    '''Return 1 frame of video
    '''
    def __init__(self):
        #self.cap = ##initialize member variable
        self.vidcap = None

    def registVideo(self, path):
        #Open Video by parameter path (string type)
        self.vidcap = cv2.VideoCapture(path)

    def getThisFrame(self):
        #Return current 1 frame
        res, img = self.vidcap.read()
        return img

    def isOpened(self):
        return self.vidcap.isOpened()




    