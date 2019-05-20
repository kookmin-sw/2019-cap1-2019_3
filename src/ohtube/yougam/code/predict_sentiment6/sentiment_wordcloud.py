from wordcloud import WordCloud
import numpy as np
from PIL import Image
import os

def wordcloud(comment_dict, reply_dict, vid):
    print(os.getcwd())
    print(comment_dict)
    print(reply_dict)
    print(vid)
    classfied_dict = {'neutral':"", 'happy':"",'sad':"",'surprise':"", 'anger':"", 'fear':""}

    for id in comment_dict:
        if comment_dict[id]['label'] == 'neutral':
            classfied_dict['neutral'] += comment_dict[id]['comment']  + ' '
        elif comment_dict[id]['label'] == 'happy':
            classfied_dict['happy'] += comment_dict[id]['comment'] + ' '
        elif comment_dict[id]['label'] == 'sad':
            classfied_dict['sad'] += comment_dict[id]['comment'] + ' '
        elif comment_dict[id]['label'] == 'surprise':
            classfied_dict['surprise'] += comment_dict[id]['comment'] + ' '
        elif comment_dict[id]['label'] == 'anger':
            classfied_dict['anger'] += comment_dict[id]['comment'] + ' '
        elif comment_dict[id]['label'] == 'fear':
            classfied_dict['fear'] += comment_dict[id]['comment'] + ' '


    for id in reply_dict:
        if reply_dict[id]['label'] == 'neutral':
            classfied_dict['neutral'] += reply_dict[id]['comment']  + ' '
        elif reply_dict[id]['label'] == 'happy':
            classfied_dict['happy'] += reply_dict[id]['comment'] + ' '
        elif reply_dict[id]['label'] == 'sad':
            classfied_dict['sad'] += reply_dict[id]['comment'] + ' '
        elif reply_dict[id]['label'] == 'surprise':
            classfied_dict['surprise'] += reply_dict[id]['comment'] + ' '
        elif reply_dict[id]['label'] == 'anger':
            classfied_dict['anger'] += reply_dict[id]['comment'] + ' '
        elif reply_dict[id]['label'] == 'fear':
            classfied_dict['fear'] += reply_dict[id]['comment'] + ' '

    icon = "youtube_icon"
    icon_path = "yougam/static/wordcloud_dataset/%s.png" % icon
    font = "BMHANNAPro"
    font_path = "yougam/static/wordcloud_dataset/%s.ttf" % font
    icon = Image.open(icon_path)
    mask = Image.new("RGB", icon.size, (255,255,255))
    mask.paste(icon,icon)
    mask = np.array(mask)

    wordcloud = WordCloud(
        font_path=font_path,
        background_color='white',
        width = 513,
        height = 512,
        mask=mask,
        colormap="Dark2",
        )

    for senti in classfied_dict:
        if len(classfied_dict[senti]) != 0:
            text = classfied_dict[senti]
            wordcloud.generate(text)
            save_path = 'yougam/static/wordcloud_dataset/wordcloud_img/' + senti + '/%s_%s.png' % (vid,senti)
            wordcloud.to_file(save_path)
