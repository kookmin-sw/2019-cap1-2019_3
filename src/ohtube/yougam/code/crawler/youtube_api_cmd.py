import json
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen
import ssl

YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'


class YouTubeApi():

    def __init__(self, max, videourl, key):
        self.max = max
        self.videourl = videourl
        self.key = key
        self.comments = dict()
        self.cmt_idx = 1

    def load_comments(self, mat):

        for item in mat["items"]:
            comment_dict = {}
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            like = comment["snippet"]["likeCount"]
            date = comment["snippet"]["publishedAt"]

            # print("Comment by {}: {}, like: {}, date: {}".format(author, text, like, date))
            comment_dict["comment"] = text
            comment_dict["author"] = author
            comment_dict["period"] = date
            comment_dict["like"] = like

            if 'replies' in item.keys():
                replies = {}
                reply_id = 1
                for reply in item['replies']['comments']:
                    reply_dict = {}
                    rauthor = reply['snippet']['authorDisplayName']
                    rtext = reply["snippet"]["textDisplay"]
                    rlike = reply["snippet"]["likeCount"]
                    rdate = reply["snippet"]["publishedAt"]

                    reply_dict["comment"] = rtext
                    reply_dict["author"] = rauthor
                    reply_dict["period"] = rdate
                    reply_dict["like"] = rlike
                    replies[reply_id] = reply_dict
                    reply_id += 1

                comment_dict["replies"] = replies
                # print(comment_dict)

            # print(comment_dict)
            self.comments[self.cmt_idx] = comment_dict
            self.cmt_idx += 1


    def get_video_comment(self):
        mxRes = 20
        vid = str()

        if not self.max:
            self.max = mxRes

        if not self.videourl:
            exit()

        if not self.key:
            exit()

        try:
            video_id = urlparse(str(self.videourl))
            q = parse_qs(video_id.query)
            vid = q["v"][0]

        except:
            print("Invalid YouTube URL")

        parms = {
                    'part': 'snippet,replies',
                    'maxResults': self.max,
                    'videoId': vid,
                    'textFormat': 'plainText',
                    'key': self.key
                }

        try:

            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            i = 2
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")
            self.load_comments(mat)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                # print("\nPage : ", i)
                # print("------------------------------------------------------------------")

                self.load_comments(mat)
                i += 1
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")
        #
        print(self.comments)
        return self.comments


    def get_video_title(self):
        vid = str()
        video_id = urlparse(str(self.videourl))
        q = parse_qs(video_id.query)
        vid = q["v"][0]

        parms = {
                    'part': 'snippet',
                    'id': vid,
                    'key': self.key
                }
        matches = self.openURL(YOUTUBE_VIDEO_URL, parms)
        mat = json.loads(matches)

        return(mat["items"][0]["snippet"]["title"])


    def openURL(self, url, parms):
            context = ssl._create_unverified_context()
            f = urlopen(url + '?' + urlencode(parms), context=context)
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches

def main():
    y = YouTubeApi(100,'https://www.youtube.com/watch?v=r4fvSf4xGU4','')
    y.get_video_comment()

if __name__ == '__main__':
    main()
