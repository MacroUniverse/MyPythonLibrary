import file
def exec_debug(s):
	try:
		exec(s)
	except Exception as e:
		print(str(e))
		file.filewrite('exec_debug.py', s) # for debugging
		print('check that line in exec_debug.py')
