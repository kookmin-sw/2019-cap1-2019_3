from ImgLoader import ImgLoader
from Receiver import Receiver

class Sender:
    def __init__(self):
        self.imgLoader = ImgLoader()
        self.receiver = Receiver()

    def send_path(self, path):
        self.receiver.video_service(path)

    def send_imgs(self, path):
        self.imgLoader.registVideo(path)
        for i in range(1000):
            if i==0 or i==99 or i==999:
                img = self.imgLoader.getThisFrame()
                self.receiver.web_cam_service(img)
            else:
                self.imgLoader.getThisFrame()



