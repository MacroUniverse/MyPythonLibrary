#!/usr/bin/python3

# usage:
# find . -type f -name *.matt -exec ./rename.py {} +
import os, glob, sys

N = len(sys.argv)
count = 0
for i in range(1,N):
	fname = sys.argv[i]
	beg = fname.rfind('/')
	#print(fname)
	#print('beg = ', beg)
	if beg >= 0:
		if fname[beg-8:beg] == 'analysis':
			beg += 1
		else:
			continue
	else:
		beg = 0
	
	if len(fname) < 5 or fname[-5:] != '.matt':
		continue
	if fname[beg:beg+6] == 'P_r1r2':
		newname = fname[:beg] + 'Pr1r2_' + fname[beg+6:]
		count += 1
		print(count, fname + ' -> ' + newname)
		os.rename(fname, newname)
	elif fname[beg:beg+11] == 'single_prob':
		newname = fname[:beg] + 'P2_' + fname[beg+11:]
		count += 1
		print(count, fname + ' -> ' + newname)
		os.rename(fname, newname)

print(count, 'files renamed!\n')
