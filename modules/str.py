def get_line(str, start):
	ind = str.find('\n', start)
	if ind >= 0:
		return str[start:ind]
	else:
		return str[start:]
