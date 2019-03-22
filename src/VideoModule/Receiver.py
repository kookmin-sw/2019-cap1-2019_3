from Commander import Commander
from ImgLoader import ImgLoader

class Receiver:
    def __init__(self):
        self.commander = Commander()
        self.imgLoader = ImgLoader()

    def video_service(self, path):
        self.imgLoader.registVideo(path)
        print("Video opened at server(Receiver).")
        for i in range(1000):
            if i==0 or i==99 or i==999:
                img = self.imgLoader.getThisFrame()
                self.commander.mainLogic(img)
            else:
                self.imgLoader.getThisFrame()


    def web_cam_service(self,img):
        print("One img arrival at server.")
        self.commander.mainLogic(img)


    