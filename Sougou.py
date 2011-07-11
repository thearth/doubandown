#!/usr/bin/env python
#-*- coding:utf-8 -*-
from Compare import compare
import urllib,urllib2,re

class EndOfPage(Exception) :
	pass

def matchrule(urlhandle,mark,rule) :
	while True :
		line = urlhandle.readline().decode('GBK').encode('utf-8')
		if not line : raise(EndOfPage())
		if line.find(mark)>0 :
			match = rule.search(line)
			if match :
				return match.group(2)
			else : print line
				

def capture(urlhandle) :
	mark = ['<td class="songname">','showSinger','singger','window.open','dl"><a href']
	rerule = []
	name = re.compile(r'(\btitle=")(.+)(" action)')
	rerule.append(re.compile(r'(\btitle=")(.*)(" action)'))
	rerule.append(re.compile(r'(\btitle=")(.*)(" target)'))
	rerule.append(re.compile(r'(\btitle=")(.*)(" target)'))
	rerule.append(re.compile(r"(open\('/)(.+)(','','width)"))
	rerule.append(re.compile(r'(href=")(.+)(" class=)'))
	while True :
		
		result = []
		try :
			for i,rule in enumerate(rerule[:-2]) : 
				result.append(matchrule(urlhandle,mark[i],rule))
			downpage = 'http://mp3.sogou.com/'+matchrule(urlhandle,mark[-2],rerule[-2])
			handle = urllib.urlopen(downpage)
			result.append(matchrule(handle,mark[-1],rerule[-1]))
			yield result
		except EndOfPage:
			return
				

def select(song,album,singer) :
	url = "http://mp3.sogou.com/music.so?query=%s" % song.decode('utf-8').encode('GBK')	#搜索歌曲，汉字及日本字符需要转码
	urlhandle = urllib.urlopen(url)
	linklist = []

	for csong,csinger,calbum,downlink in capture(urlhandle) :
		distinction = compare(csong,song)+compare(calbum,album)+compare(csinger,singer) 
		linklist.append((distinction,downlink))
	return linklist
