#coding=UTF-8
import os
import urllib
import urllib2
import json

def get_tuling(text):
	#"http://www.tuling123.com/openapi/api?key=3a09978701b14d58904941eb4253bf3c&info=北京天气"
	api_str = "http://www.tuling123.com/openapi/api?key=3a09978701b14d58904941eb4253bf3c&info="
	url = api_str+text
	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	res = json.loads(res)
	return res["text"]
	#{"code":100000,"text":"北京:周六 10月7日,小雨 东北风,最低气温13度，最高气温20度"}

#text="北京天气"
#print get_tuling(text)
