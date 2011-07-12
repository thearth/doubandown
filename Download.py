#!/usr/bin/env python

import urllib
import time
import threading
import signal
import os

piece = 4096
lock = threading.RLock()
lockd = threading.RLock()


class CanNotDownload(Exception) :
	def __init(self) :
		pass

class Die():
	def __init__(self) :
		self.die = -20
	def isdie(self) :
		if self.die > 0 : return True
		else : return False
	def godie(self) :
		self.die += 1

class Downfile() :
	name = ''
	def setname(self,string) :
		self.name = string
	def delete(self) :
		print 'Trying to remove',self.name
		if os.path.isfile(self.name) : os.remove(self.name)

downfile = Downfile()
die = Die()

def func_sig(a,b):
	downfile.delete()
	os.abort()

signal.signal(signal.SIGUSR1,func_sig)


class partdown(threading.Thread):
	def __init__(self,url,span,filehandle) :
		self.url = url
		self.begin,self.end = span
		self.downloaded = 0
		self.filehandle = filehandle
		threading.Thread.__init__(self)


	def run(self) :
		self.downloaded = self.begin
		opener = urllib.FancyURLopener()
		opener.addheader("Range","bytes=%d-%d" % (self.begin,self.end))
		urlhandle = opener.open(self.url)
		data = 1
		while data :

			if die.isdie() : return
			tig = time.time()
			lock.acquire()
			data = urlhandle.read(piece)
			self.store(data)
			lock.release()
			if time.time()-tig >= 5 :
				lockd.acquire()
				die.godie()
				lockd.release()


	def store(self,data):
		self.filehandle.seek(self.downloaded)
		self.filehandle.write(data)
		self.downloaded += piece


def getfilesize(url) :
	urlhandle = urllib.urlopen(url)
	headers = urlhandle.info().headers
	length = 0
	for header in headers :
		if header.find('Length') >= 0:
			length = header.split(':')[-1].strip()
			length = int(length)
	if not length : raise CanNotDownload()
	return length


def splitblocks(totalsize,blockcount) :
	blocksize = totalsize/blockcount
	ranges = []
	for i in range(0,blockcount-1) :
		ranges.append((i*blocksize,(i+1)*blocksize-1))
	ranges.append((blocksize*(blockcount-1),totalsize-1))
	return ranges


def begin_download(url,filename,threadcount) :

	downfile.setname(filename)
	try :
		filelength = getfilesize(url)
		filehandle = open(filename,'wb')
		ranges = splitblocks(filelength,threadcount)
		tasks = []
		for i in range(0,threadcount) :
			tasks.append(partdown(url,ranges[i],filehandle))
			tasks[-1].setDaemon(True)
			tasks[-1].start()
		for task in tasks :
			task.join()
		if die.isdie() : raise CanNotDownload()
		return True
	except :
		print 'Try to delete',filename
		if os.path.isfile(filename) : os.remove(filename)
		return False

#		print 'Download %s\t complete cost %fs' % (filename,time.time()-starttime)

if __name__=='__main__' :
	url = 'http://de.xiaohe.info/COFFdD0xMzA5ODc2NjM5Jmk9MTAuMTEuMTkyLjUmdT1Tb25ncy92Mi9mYWludFFDLzg0LzFkL2VlZGRlZWQ3YTdkNDRlOGYxODE0NDk5ZTdjZjAxZDg0LndtYSZtPWY3ZDc4YjQwNzg4ZjQ4MDk1ZmZkODc5ODI1OThmMjk5JnY9ZG93biZuPc7StcS6o9HzJnM9ztK1xLqj0fMmcD1l.wma' 
	begin_download(url,'song1.wma',5)
