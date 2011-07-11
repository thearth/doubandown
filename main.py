#!/usr/bin/env python

import grab,getsong
import os

if __name__=='__main__' :
	if not (os.path.isfile('songlist')) : grab.main()
	else :
		choice = raw_input('songlist has already exists, reload from douban?(y/n)')
		if choice == 'y' : grab.main()
	getsong.main()
	
