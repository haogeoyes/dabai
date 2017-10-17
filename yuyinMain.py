#coding=UTF-8
'''
	v1.1 实现图灵机器人语音聊天
	v2.1 增加声音监测录音功能
	v3.0 使用按钮录音提升准确率
	v3.1  增加儿歌
	v3.2  增加分词 匹配任意歌曲
'''
import urllib, urllib2
import os
import sys
import json
import re
reload(sys)
sys.setdefaultencoding('utf-8')

from aip import AipSpeech
from yuyinHecheng import *
from yuyinJiexi import *
from tuling import *

import RPi.GPIO as GPIO
from time import sleep

import jieba.posseg as pseg   #词性标注

from random import choice     #随机


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


#匹配 故事 儿歌组 随机选出一首播放  返回id
def searchGroupSuiji(sear_var):
        out = readJson('mp3.json')
        text=[]
        for i in out:
                if i["name"] == None:
                        continue
                if sear_var in i["name"]:
                        for j in i["list"]:
                                text.append(i["id"])
        return text
#sear_var="故事"
#out=searchGroupSuiji(sear_var)
#print choice(out)



#分词转化为词性
def cipin_list_tag(strs):
        out={}
        cipin_object=pseg.cut(strs)
        for i in cipin_object:
                if i.word not in out:
                        out[i.word]=i.flag
        return out

#searchName("爸爸")

#获取知道问答结果
def zhiDao(url):
  try:
        page = urllib.urlopen(url)
        html = page.read()
        html = re.findall(r'<div class="list-inner">(.*?)</div>',html,re.S|re.M)
        html = re.findall(r'<dd class="dd answer">(.*?)</dd>',html[0],re.S|re.M)
        html = re.findall(r'.*</i>(.*)',html[0])
        html = unicode(html[0],"gb2312").encode("utf8")
        html = re.sub('<.*?>','',html)
        return(html)
  except Exception,e:
        return("对不起，我不知道")






#----------------------main------------------------
print "启动"

pin = 3

#基于引脚
GPIO.setmode(GPIO.BOARD)


pin_btn = 7
GPIO.setup(pin_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(pin,GPIO.IN)
status = 0	#判断录音状态0未录音 1录音
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
                        print out["result"][0] 	#说的话

                        #图灵获取问答结果
                        #text=out["result"][0]
                        #out=get_tuling(text)
                        #print out

			#搜索儿歌
			erge_status=False	#定义是否执行该动作
			action=['放','听','讲','唱']
			action_option=['故事','儿歌','童话','童声','童谣']
			for i in action:
				if i in out["result"][0]: 
					erge_status=True

                        if erge_status:		#监听到 音频动作
				speaks=cipin_list_tag(out["result"][0])
				for k in speaks:
					if k in action_option:
						#continue		#如果包含 故事 儿歌，随机播放儿歌 故事
						id_list=searchGroupSuiji(k) #返回所有包含故事 或者儿歌的 音乐id list
						id=choice(id_list)	#随机播放一首
						os.popen('omxplayer -o local http://47.94.156.180/static/mp3/data/%s.mp3 & '%id)
						break
					#查找所有音频关键词
					if speaks[k]=="n" or speaks[k]=="nr" or speaks[k]=="l" or speaks[k]=="nrt":
						id=searchName(text)
						os.popen('omxplayer -o local http://47.94.156.180/static/mp3/data/%s.mp3 & '%id)



			#知道问答
			ask_status=False	#判断语句中是否包含这些关键词
			action=['问','告诉我','问题','你知道','为什么','怎么办','多少','多远','多大','多近','谁','知道']
			for i in action:
				if i in out["result"][0]:
					ask_status=True
			if ask_status:
				word = out["result"][0]
				url="https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word="+word
				request_text=zhiDao(url)
                        	yuyin_hecheng(request_text)	#文字翻译成语音





                        #文字翻译成语音
                        soundTxt="你能再说一遍吗"
                        yuyin_hecheng(soundTxt)
		else:
                        yuyin_hecheng("好哥，我没有听清")

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
	sleep(0.05)
