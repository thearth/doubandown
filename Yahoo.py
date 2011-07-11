#!/usr/bin/env python
#-*- coding:utf-8 -*-
from Compare import compare
import urllib,urllib2,re

class EndOfPage(Exception) :
	pass


def capture(urlhandle) :
	marks = ['name="doc3_gq"','name="doc3_gs"','name="doc3_gq"']
	urlrule = re.compile('&url=(.+?)"')
	content_rule_list = re.compile('>(.*?)<')
	while True :
		
		result = []
		i = 0
		try :
			while True :
				line = urlhandle.readline()
				if not line : raise(EndOfPage())
				if line.find(marks[i])>0 :
					if i == 0: 
						match = urlrule.search(line)
						if match : link = match.group(1)
						else : print line
					context_list = content_rule_list.findall(line)
					result.append(''.join(context_list))
					i += 1
					if i> 2 : 
						break
			result.append(urllib2.unquote(link))
			yield result
		except EndOfPage:
			return
				

def select(song,album,singer) :
	url = "http://music.yahoo.cn/s?q=%s" % song	#搜索歌曲，汉字及日本字符需要转码
	urlhandle = urllib.urlopen(url)
	linklist = []

	for csong,csinger,calbum,downlink in capture(urlhandle) :
		distinction = compare(csong,song)+compare(calbum,album)+compare(csinger,singer) 
		linklist.append((distinction,downlink))
	return linklist

if __name__ == '__main__' :
	link_list = select('Big, Big World','Big Big World','Emilia')
	for distinction,link in link_list : print distinction,link
