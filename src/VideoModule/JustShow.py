from Sender import Sender

class JustShow:
    def __init__(self):
        self.sender = Sender()

    def showMenu(self):
        selectNumber = -1
        while True:
            print()
            print()
            print("...................................................................")
            print("Choose Menu")
            print("...................................................................")
            print("Service 1. open image on server.")
            print("Service 2. send image to server.")
            print("0. end")
            print("...................................................................")
            selectNumber = int(input("Input Menu Number. "))

            if selectNumber == 0:
                print("end. bye.")
                break

            elif selectNumber == 1:
                print("you select Service 1.")
                path = self.inputPath()
                self.sender.send_path(path)

            elif selectNumber == 2:
                print("you select Service 2.")
                path = self.inputPath()
                self.sender.send_imgs(path)

            else:
                print("Choose again!")

    def inputPath(self):
        path = str(input("input video's path. "))
        return path

