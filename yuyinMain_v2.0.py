#coding=UTF-8
'''
	v1.1 增加声音监测录音功能
'''
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')  
from aip import AipSpeech
from yuyinHecheng import *
from yuyinJiexi import *
from tuling import *

import RPi.GPIO as GPIO
from time import sleep




pin = 3

#基于引脚
GPIO.setmode(GPIO.BOARD)


GPIO.setup(pin,GPIO.IN)
while True:
	if GPIO.input(pin) == 0:
		print "监测到声音"
		#录音
		os.popen('omxplayer readyAsk.mp3')
		os.popen('omxplayer tishi.mp3')
		print "开始录音"
		os.popen('arecord -D "plughw:1,0" -r16000 -f S16_LE -d 2 test.wav')
		print "开始识别"
		os.popen('omxplayer tishi.mp3')

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
	sleep(0.05)
