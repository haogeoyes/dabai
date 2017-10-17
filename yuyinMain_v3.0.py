#coding=UTF-8
'''
	v1.1 实现图灵机器人语音聊天
	v2.1 增加声音监测录音功能
	v3.0 使用按钮录音提升准确率
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


pin_btn = 7
GPIO.setup(pin_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(pin,GPIO.IN)
status = 0
while True:
	if GPIO.input(pin_btn) == 1 and status == 1:
		os.popen('cp test.wav speak.wav ')
		os.popen("ps -ef | grep test.wav | grep -v 'grep' | awk  '{print $2}' | xargs kill -9 &")
		os.popen('omxplayer /home/pi/me/yuyin/tishi.mp3 &')
		#os.popen('omxplayer speak.wav &')
		status = 0
                #语音解析成文字
                soundFile='speak.wav'
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
	if GPIO.input(pin_btn) == 0 and status == 0:
		print "监测到声音"
		#录音
		#os.popen('omxplayer readyAsk.mp3')
		os.popen('omxplayer /home/pi/me/yuyin/tishi.mp3 &')
		print "开始录音"
		os.popen('arecord -D "plughw:1,0" -r16000 -f S16_LE -d 2000000 test.wav &')
		status = 1
		sleep(1)
		#os.popen('omxplayer tishi.mp3')
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
