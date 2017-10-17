#coding=UTF-8
from aip import AipSpeech
import os
def yuyin_jiexi(soundFile):
	APP_ID = '7647466'
	API_KEY = 'CCyo6UGf16ggKZGwGpQYL9Gx'
	SECRET_KEY = '8f4b63a694bec01c3be063ca6c7cfe17'

	aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

	# 读取文件
	def get_file_content(filePath):
	    with open(filePath, 'rb') as fp:
	        return fp.read()

	# 识别本地文件
	out=aipSpeech.asr(get_file_content(soundFile), 'wav', 16000, {
	    'lan': 'zh',
	})
	return out

'''
#录音
os.popen('omxplayer readyAsk.mp3')
os.popen('omxplayer tishi.mp3')
print "开始录音"
os.popen('arecord -D "plughw:1,0" -r16000 -f S16_LE -d 2 test.wav')
print "开始识别"
os.popen('omxplayer tishi.mp3')

soundFile='test.wav'
out=yuyin_jiexi(soundFile)
print out["err_no"]
if out["err_no"]==0:
	print out["result"][0]
'''




