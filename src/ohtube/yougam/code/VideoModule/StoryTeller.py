from JustShow import JustShow

class StoryTeller:

    def __init__(self):
        self.justShow = JustShow()

    def startStory(self):
        self.justShow.showMenu()

if __name__ == "__main__":
    storyTeller = StoryTeller()
    storyTeller.startStory()