#!/usr/bin/python3

# scan through all mp4 and mov files in the current directory and subdirectory. If the bitrate is larger than 500kbps, compress it to 500kbps.

import os
import sys
import shutil
import subprocess

def compress_file(full_path):
	"""Compress a file to a certain bitrate using ffmpeg."""
	directory, filename = os.path.split(full_path)
	full_path_out = os.path.join(directory, 'ffzip_' + filename)
	cmd = f'ffmpeg -y -i "{full_path}" -max_muxing_queue_size 10000 -b:v 500k "{full_path_out}" > /dev/null 2>&1'
	res = subprocess.run(cmd, shell=True)
	return res.returncode, full_path_out

def scan_files(directory):
	if not os.path.exists(directory):
		print("no such directory: ", directory)
		sys.exit()
	if not os.path.exists('./recycle'):
		os.makedirs('./recycle')
	"""Scan a directory and its subdirectories for mp4 and mov files."""
	for foldername, subfolders, filenames in os.walk(directory):
		if foldername == './recycle':
			continue
		for filename in filenames:
			if (filename.startswith('RPReplay') or filename.startswith('Screen_Recording')) and (filename.endswith('.mp4') or filename.endswith('.mov') or filename.endswith('.MP4') or filename.endswith('.MOV')):
				full_path = os.path.join(foldername, filename)
				print('\n\n', full_path)
				print('-----------------------------------------------------------')
				exit_code, full_path_out = compress_file(full_path)
				if exit_code != 0:
					print('failed!')
					try:
						os.remove(full_path_out)
					except:
						pass
					continue
				out_path = './recycle/' + filename
				while os.path.exists(out_path):
					out_path = '1' + out_path
				shutil.move(full_path, out_path)
	
	# delete `./recycle` if it's empty
	if os.path.exists('./recycle') and not os.listdir('./recycle'):
		os.rmdir('./recycle')

# Start scanning from the current directory
scan_files('.')
