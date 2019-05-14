from Commander import Commander
from ImgLoader import ImgLoader

class Receiver:
    def __init__(self):
        self.commander = Commander()

    def video_service(self, path):
        self.commander.mainLogic(path)

    def web_cam_service(self,img):
        print("One img arrival at server.")
        self.commander.mainLogic(img)


    