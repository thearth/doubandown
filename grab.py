#!/usr/bin/python
#-*- coding:UTF-8 -*-
import time
import math
import os
import re
import urllib
import urllib2
import cookielib
import time

class robot:

	def __init__(self,email,passwd):
		print 'now init'

		self.form = {
			'source':'radio',
			'form_email': email,
			'form_password':passwd,
			'remember':'on',
		}
		self.login_path = 'http://www.douban.com/accounts/login'
		self.songlist = []

		self.cj = cookielib.CookieJar()		# set a cookie
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))	#build a opener
		urllib2.install_opener(self.opener)	# install a opener
		self.opener.addheaders = [('User-agent','Opera/9.23')]	# add header to opener


	def login(self):
		print 'now login'
		while True :

			response = urllib2.Request(self.login_path,urllib.urlencode(self.form))		# request a url with post data
			print urllib.urlencode(self.form)
			url = self.opener.open(response).geturl()
			print url
			if url.find('douban.fm')>=0 :												#分析返回的url看是否已经登录成功
				print 'Login success !'
				return True
			else :
				for line in urllib2.urlopen(response) :
					match = re.search(r'(<img src=")(.+)(" alt="captcha")',line)		#查找验证码地址
					if match :
						captchaurl = match.group(2)
						print captchaurl
						urllib.urlretrieve(captchaurl,'capthca.jpg')					#下载验证码
						captcha = raw_input('input the capthca : ')						#用户输入验证码
						self.form['captcha-solution'] = captcha
						self.form['captcha-id'] = captchaurl.split('=')[1].split('&')[0]
						break;
				else :
					return False


	def fetchall(self):
		pos = 0
		i = 0
		flag = False
		total = 32767
		rules = []
		rules.append(re.compile(r'(\d+)(首喜欢的</span>)'))									#详细添加各个匹配规则
		rules.append(re.compile(r'(<td>)(.+)(</td>)'))
		rules.append(re.compile(r'(title=")(.*)(">)'))
		rules.append(re.compile(r'(<span>)(.*)(</span>)'))
		
		while (pos<=total) :
			operator = urllib2.Request('http://douban.fm/mine?start=%d&type=liked' % (pos))
			page = urllib2.urlopen(operator)												#-------------------------------#
			for line in page :                                                              #啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊 #
				if not flag :                                                               #这段代码写的尤其恶心           #
					match = rules[i].search(line)                                           #而且这已经是我第二次           #
					if match :                                                              #重构这段代码了                 #
						total = int(match.group(1))                                         #可是本身网页上这段逻辑         #
						flag = True                                                         #就不是很规整                   #
						i += 1                                                              #歌明单独占一行                 #  
						continue                                                            #而专集和歌手却既在一行         #     
				else :                                                                      #我也没有办法啊                 #
					match = rules[i].search(line)                                           #所以这段不规则的分支就这么多   #    
					if match :                                                              #有谁能帮我简化简化             #
						if i == 1 :                                                         #就帮我简化简化吧               #
							song = match.group(2)                                           #出去了不要说这段是我写的       #
							if not song : song = ' '										#								#
							i += 1                                                          #梦游                           #
							continue                                                        #梦游                           #
						elif i == 2 :                                                       #梦游                           #
							album = match.group(2)                                          #梦游                           #
							if not album : album = ' '										#								#
							singer = rules[i+1].search(line).group(2)                       #哦耶，占满了                   #    
							if not singer : singer = ' '									#								#
							i -= 1															#-------------------------------#
							self.songlist.append((song,album,singer))
			pos += 9

def main() :

#	filehandle = open('logdata.ini')						#读入用户信息
#	for line in filehandle.readlines() :
#		if line.find('email')>=0 :
#			email = line.split('=')[-1].strip().rstrip()
#		if line.find('passwd')>=0 :
#			passwd = line.split('=')[-1].strip().rstrip()
	for i in range(3) : 
		email = raw_input('E-mail Account : ')
		os.system('stty -echo')
		passwd = raw_input('Password : ')
		os.system('stty echo')
		app = robot(email,passwd)								#初始化登录机器人
		if app.login() : break

	app.fetchall()
	print 'Totally find',len(app.songlist),'songs'

	filehandle = open('songlist','w')						#存储歌曲信息
	for name,album,singer in app.songlist :
		filehandle.write(name+'\t'+album+'\t'+singer+'\n')

if __name__ == '__main__' :
	main()
