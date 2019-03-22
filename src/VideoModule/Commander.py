import cv2

class Commander:
    def __init__(self):
        pass

    def mainLogic(self, img):
        if img != None:
            cv2.imshow("image", img)
            cv2.waitKey(1000)#pause for 1 second
            cv2.destroyAllWindows()
        else:
            print("Img has not been received")






