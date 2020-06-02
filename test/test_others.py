import sys
sys.path.insert(1, '../modules/')
from others import *
from file import *

s = '''print('now in script.py:1')
print('now in script.py:2')
print('now in script.py:3')
print('now in script.py:4')
'''

exec_debug(s)
