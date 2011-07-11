#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib,urllib2,re
import Download,Sougou,Yahoo
import os



class songlist():
	slist = []
	namelist = []

	def __init__(self,filename) :
		filehandle = open(filename,'r')
		for line in filehandle.readlines() :
			song,album,singer = line.split('\t')
			self.slist.append((song,album,singer.rstrip()))
			self.namelist.append(song)


def filterlist(songs,songlist,current_path) :
	songs.sort()
	i,j = 0,0
	for filelist in os.walk(current_path) : filelist = filelist[2]
	filelist.sort()
	result = []
	lens,lenf = len(songs),len(filelist)
	while i<lens and j<lenf :
		song = songs[i]
		flag = cmp(song,os.path.splitext(filelist[j])[0])
		if flag>0 : j += 1
		elif flag==0 : i,j = i+1,j+1
		else :
			result.append(songlist[i])
			i += 1
	result += songlist[i:]
	return result


def search(songs) :
	process = 5								#最大进程数
	total = len(songs.slist)
	notfoundlist = []						#未找到歌曲列表
	i,j = 0,0
	PS = {}									#进程pid与歌曲名字的字典
	current_path = os.getcwd()
	songlist = filterlist(songs.namelist,songs.slist,current_path) 
	print len(songlist)
	path = raw_input('Path to download : ')
	if not os.path.exists(path) : os.mkdir(path)
	os.chdir(path)

	try :
		for (i,(song,album,singer)) in enumerate(songs.slist) :
			if process <= 0:
				pid,failed = os.wait()
				process += 1
				if failed :
					print 'Download Failed in',song
					notfoundlist.append(PS[pid])
					del PS[pid]

			process -= 1
			pid = os.fork()
			if not pid :
				print '%3d now trying to download %s' % (i,song)
				linklist = Sougou.select(song,album,singer)+Yahoo.select(song,album,singer)#+Top100.select(song,album,singer)
				if not linklist : exit(1)
				linklist.sort()
				for distinction,downlink in linklist[:3] :
					exname = downlink.split('.')[-1].rstrip().lower().split('?')[0]
					filename = song+'.'+exname
					if Download.begin_download(downlink,filename,5) :
						print 'Download complete : ',song
						exit()
					else :
						print 'Download crashed : ',song,'\tTry to download from another source'
				exit(1)
			else :
				PS[pid]=(song,album,singer)


		for key in PS.keys() :
			pid,failed = os.wait()
			process += 1
			if failed :
				print 'Download Failed in',song
				notfoundlist.append(PS[pid])
				del PS[pid]

	except KeyboardInterrupt :
		for key in PS.keys() :
			print key
			os.kill(key,9)
	
	
	if notfoundlist :											#输出未找到的歌曲
		print 'Failed to find following songs'
		for song,album,singer in notfoundlist :
			print song+'\t'+album+'\t'+singer

def main() :
	songs = songlist('songlist')
	search(songs)


if __name__=='__main__' :
	main()
