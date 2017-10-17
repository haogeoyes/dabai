#coding=UTF-8
'''
	v1.1 实现图灵机器人语音聊天
	v2.1 增加声音监测录音功能
	v3.0 使用按钮录音提升准确率
	v3.1  增加儿歌
'''
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
from aip import AipSpeech
from yuyinHecheng import *
from yuyinJiexi import *
from tuling import *

import RPi.GPIO as GPIO
from time import sleep


#----------------------fun------------------------
#读json
def readJson(filename):
    if os.path.exists(filename):
        with open(filename,'r') as file_object:
                contents = json.load(file_object)
        return contents
    else:
        return []


#搜索所有歌曲
def searchName(sear_var):
        out = readJson('mp3.json')
        for i in out:
                for j in i["list"]:
                        if sear_var in str(j["name"]):
                                print j["id"]
                                print j["name"]
                                filename = "./data/"+str(j["id"])+".mp3"
                                print os.path.exists(filename)
				return j["id"]

#searchName("爸爸")






#----------------------main------------------------

pin = 3

#基于引脚
GPIO.setmode(GPIO.BOARD)


pin_btn = 7
GPIO.setup(pin_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(pin,GPIO.IN)
status = 0
while True:
	if GPIO.input(pin_btn) == 1 and status == 1:
		os.popen('cp test.wav speak.wav ')
		os.popen("ps -ef | grep test.wav | grep -v 'grep' | awk  '{print $2}' | xargs kill -9 &")
		os.popen('omxplayer -o local /home/pi/me/yuyin/tishi.mp3 &')
		#os.popen('omxplayer -o local speak.wav &')
		status = 0
                #语音解析成文字
                soundFile='speak.wav'
                out=yuyin_jiexi(soundFile)
                if out["err_no"]==0:
                        print out["result"][0]

                        #图灵获取问答结果
                        #text=out["result"][0]
                        #out=get_tuling(text)
                        #print out

			#搜索儿歌
			text=out["result"][0]
			text=text.split('，')[0]
			print text

			id=searchName(text)
			os.popen('omxplayer -o local http://47.94.156.180/static/mp3/data/%s.mp3 & '%id)

                        #文字翻译成语音
                        soundTxt=id
                        yuyin_hecheng(soundTxt)
	if GPIO.input(pin_btn) == 0 and status == 0:
		print "监测到声音"
		#录音
		#os.popen('omxplayer -o local readyAsk.mp3')
		os.popen("ps -ef | grep omxplayer | grep -v 'grep' | awk  '{print $2}' | xargs kill -9 &")
		os.popen('omxplayer -o local /home/pi/me/yuyin/tishi.mp3 &')
		print "开始录音"
		os.popen('arecord -D "plughw:1,0" -r16000 -f S16_LE -d 2000000 test.wav &')
		status = 1
		sleep(1)
		#os.popen('omxplayer  -o local tishi.mp3')
		'''
		#语音解析成文字
		soundFile='test.wav'
		out=yuyin_jiexi(soundFile)
		if out["err_no"]==0:
			print out["result"][0]
				
			#图灵获取问答结果
			text=out["result"][0]
			out=get_tuling(text)
			print out

			#文字翻译成语音
			soundTxt=out
			yuyin_hecheng(soundTxt)
		'''
	sleep(0.05)
