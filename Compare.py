#!/usr/bin/env python

def compare(a,b) :
	a = ' '+a.lower()
	b = ' '+b.lower()
	m = len(a)
	n = len(b)
	f = [[0 for col in xrange(n)] for row in xrange(m)]
	for i in xrange(1,m) :
		for j in xrange(1,n) :
			if a[i]==b[j] : f[i][j] = f[i-1][j-1]
			else : 
				f[i][j] = min(f[i-1][j],f[i-1][j-1],f[i][j-1])+1
	return f[m-1][n-1] / float(n+m)
