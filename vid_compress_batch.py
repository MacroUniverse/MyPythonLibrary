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
	cmd = 'ffmpeg -y -i {} -b:v 500k {}'.format(full_path, full_path_out)
	subprocess.run(cmd, shell=True)

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
				out_path = './recycle/' + filename
				print('\n\n', full_path)
				print('-----------------------------------------------------------')
				compress_file(full_path)
				print(out_path)
				if os.path.exists(out_path):
					os.remove(out_path)
				shutil.move(full_path, out_path)
	
	# delete `./recycle` if it's empty
	if os.path.exists('./recycle') and not os.listdir('./recycle'):
		os.rmdir('./recycle')

# Start scanning from the current directory
scan_files('.')
