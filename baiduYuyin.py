#coding=UTF-8
from aip import AipSpeech
import os

APP_ID = '7647466'
API_KEY = 'CCyo6UGf16ggKZGwGpQYL9Gx'
SECRET_KEY = '8f4b63a694bec01c3be063ca6c7cfe17'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
soundTxt='''
我可以播放儿歌，讲故事，背三字经，还可以和你聊天
'''
result  = aipSpeech.synthesis(soundTxt, 'zh', 1, {
    'vol': 3,
    'per': 3,
})


if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
    os.popen('omxplayer auido.mp3')


