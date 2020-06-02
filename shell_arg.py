#!/usr/bin/python3
# use `./shell_arg abc dks lsk eid 123` to call

import sys

# sys.argv is a list of strings
print("calling command is:", sys.argv[0])

N = len(sys.argv)
for i in range(1, N):
	print("argument", i, "is",  sys.argv[i])
