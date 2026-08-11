#!/usr/bin/python3

#######################################
# TODO: use os.path.relpath(path2, path1) instead of chdir
# TODO: total path length on windows cannot exceed 200+!
#######################################

# ====== base 16384 ========
# used to encrypt names so that they are almost certainly shorter than original name
# code points from 19968 to 39447, sorted but not contiguous
# taken from Xinhua dictionary, see https://github.com/pwxcoo/chinese-xinhua
base16384_str = ''

# ===== what to run =======
def main():
	global base16384_str

	# ====== password =====
	password = input("Please enter password: ")
	password1 = input("Please confirm password: ")
	if password1 != password:
		print("Password doesn't match.")
		return

	with open('base16384_utf8_chinese_sorted.txt') as file:
		# Read the contents of the file
		base16384_str = file.read()
		assert len(base16384_str) == 16384

	# # example: use password = '1234'

	# print(encrypt_str_to_str64('some string', password))
	# print(decrypt_str64_to_str('tG8n+/6WJVORHEw4c2pMzA==', password))

	# print(encrypt_str_to_str16384('some string', password))
	# print(decrypt_str16384_to_str('丂變备駧榒揞喿凫崶尻', password))

	encrypt_folder('test', 'test-encrypted', password)
	# decrypt_folder('test-encrypted', 'test-decrypted', password)

	# encrypt_names_in_folder('Computational_Physics_Course', password)
	# decrypt_names_in_folder('Computational_Physics_Course', password)
# ==========================

import os
import random
import subprocess
import base64

# internal setting
file_extension = '.eNc'
len_ext = len(file_extension)
dic_file = 'enc-long-name-dic.txt'
hex_chars = '0123456789abcdef'


def encrypt(file_to_encrypt, encrypted_file, password):
	"""
	encrypt a file
	will overwrite if output file already exists
	"""
	command = [
		'openssl', 'aes-256-cbc', '-nosalt', '-pbkdf2',
		'-in', file_to_encrypt,
		'-out', encrypted_file,
		'-pass', 'pass:' + password
	]
	result = subprocess.run(command)
	if result.returncode != 0:
		print("encryption failed!")
		raise RuntimeError('encryption failed!')


def decrypt(file_to_decrypt, decrypted_file, password):
	"""
	decrypt a file
	will overwrite if output file already exists
	"""
	command = [
		'openssl', 'aes-256-cbc', '-nosalt', '-pbkdf2', '-d',
		'-in', file_to_decrypt,
		'-out', decrypted_file,
		'-pass', 'pass:' + password
	]
	result = subprocess.run(command)
	if result.returncode != 0:
		print("encryption failed!")
		raise RuntimeError('decryption failed!')


def encrypt_str_to_str64(string_to_encrypt, password):
	"""
	encrypt a string to base64 (no `\n`, with `=` padding)
	"""
	command = [
		'openssl', 'enc', '-base64', '-A', '-e', '-aes-256-cbc',
		'-nosalt', '-pbkdf2', '-pass', 'pass:' + password
	]
	result = subprocess.run(command, input=string_to_encrypt, text=True,
						 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode != 0:
		raise RuntimeError('encryption failed!')
	return result.stdout


def decrypt_str64_to_str(string_to_decrypt, password):
	"""
	decrypt a base64 string (no `\n`, with `=` padding)
	"""
	command = [
		'openssl', 'enc', '-base64', '-A', '-d', '-aes-256-cbc',
		'-nosalt', '-pbkdf2', '-pass', 'pass:' + password
	]
	result = subprocess.run(command, input=string_to_decrypt+'\n', text=True,
						 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode != 0:
		raise RuntimeError('decryption failed!')
	return result.stdout


def encrypt_str_to_str16384(string_to_encrypt, password):
	"""
	encrypt a string to base16384 (no `\n`, no padding)
	"""
	str64 = encrypt_str_to_str64(string_to_encrypt, password)
	return str64_to_strN(str64, base16384_str)


def decrypt_str16384_to_str(string_to_decrypt, password):
	"""
	decrypt a string to base16384 (no `\n`, no padding)
	"""
	str64 = strN_to_str64(string_to_decrypt, base16384_str)
	return decrypt_str64_to_str(str64, password)


def encrypt_files_in_folder(directory, out_dir, password):
	"""
	encrypt files/folders in `directory` to `out_dir`
	"""
	cwd = os.getcwd()
	out_dir = os.path.abspath(out_dir)
	try:
		os.chdir(directory)
		for root, dirs, files in os.walk('.', topdown=False):
			for name in files:
				path = os.path.join(root, name)
				root_new = os.path.join(out_dir, root)
				if not os.path.exists(root_new):
					os.makedirs(root_new)
				new_path = os.path.join(root_new, name)
				print(new_path)
				encrypt(path, new_path, password)
			for name in dirs: # for empty path
				path = os.path.join(root, name)
				root_new = os.path.join(out_dir, root)
				new_path = os.path.join(root_new, name)
				print(new_path)
				if not os.path.exists(new_path):
					os.makedirs(new_path)
	finally:
		os.chdir(cwd)


def decrypt_files_in_folder(directory, out_dir, password):
	"""
	decrypt files in `directory` to another folder `out_dir`
	"""
	cwd = os.getcwd()
	out_dir = os.path.abspath(out_dir)
	try:
		os.chdir(directory)
		for root, dirs, files in os.walk('.', topdown=False):
			for name in files:
				if (name == dic_file):
					continue
				path = os.path.join(root, name)
				root_new = os.path.join(out_dir, root)
				if not os.path.exists(root_new):
					os.makedirs(root_new)
				new_path = os.path.join(root_new, name)
				print(new_path)
				decrypt(path, new_path, password)
			for name in dirs: # for empty path
				path = os.path.join(root, name)
				root_new = os.path.join(out_dir, root)
				new_path = os.path.join(root_new, name)
				print(new_path)
				if not os.path.exists(new_path):
					os.makedirs(new_path)
	finally:
		os.chdir(cwd)


def encrypt_file_or_folder_name(path, dic_file_handle, log_file, password):
	"""
	encrypt the name of a file or folder and rename with base16384
	if the name is too long, will name it to 'long-name-xxxx.file_extension'
	and append the full name to `dic_file_handle`
	dic_file_handle = open(dic_path, 'a')
	"""
	root = os.path.dirname(path)
	name = os.path.basename(path)
	if (name[-len_ext:] == file_extension):
		return
	name_new = encrypt_str_to_str16384(name, password) + file_extension
	if len(name_new) > 220: # windows filename max size is 224
		random_hex_string = ''.join(random.choice(hex_chars) for _ in range(32))
		name_short = 'long-name-' + random_hex_string \
			+ file_extension
		dic_file_handle.write(name_short + ' ' + name_new + '\n')
		name_new = name_short
	log_line = path + ' -> ' + name_new
	print(log_line)
	log_file.write(log_line + '\n')
	os.rename(path, os.path.join(root, name_new))


def encrypt_names_in_folder(directory, password):
	"""
	encrypt names of files and subfolders inside a folder recursively (rename)
	will add `file_extension`, and skip files already with it
	for files with name too long, rename it to
	  `long-name-<id>.<file_extension>`,
	then use a `dic_file` to map to the actual
	  encrypted name `*.<file_extension>`
	"""
	dic_path = os.path.join(directory, dic_file)
	dic_file_handle = open(dic_path, 'a')
	log_file = open('encrypted_name_dict.txt', 'a')
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			if (name == dic_file):
				continue
			encrypt_file_or_folder_name(os.path.join(root, name), dic_file_handle, log_file, password)
		for name in dirs:
			if (name[-len_ext:] == file_extension):
				continue
			encrypt_file_or_folder_name(os.path.join(root, name), dic_file_handle, log_file, password)
	dic_file_handle.close()
	log_file.close()
	if os.path.exists(dic_path) and os.path.getsize(dic_path) == 0:
		os.remove(dic_path)


def decrypt_file_or_folder_name(path, long_names, password):
	"""
	decrypt the name of a file or folder from base16384
	will skip files without `file_extension`
	if the name is `long-name-xxx.file_extension`,
		will get the real encrypted name from `long_names` dictionary
	"""
	root = os.path.dirname(path)
	name = os.path.basename(path)
	if (name[-len_ext:] != file_extension):
		return
	if (name[:10] == 'long-name-'):
		try:
			name = long_names[name]
		except Exception as e:
			print('Error:', dic_file, 'key not found (will skip): ' + name)
			return
	try:
		name_new = decrypt_str16384_to_str(name[:-len_ext], password)
	except Exception as e:
		print('Error: string decryption failed: ' + name)
		return
	print(path, ' -> ', name_new)
	os.rename(path, os.path.join(root, name_new))


def decrypt_names_in_folder(directory, password):
	"""
	decrypt names of files and subfolders inside a folder recursively (rename)
	will only process files with extension file_extension
	"""
	# get dictionary `long_names`
	dic_path = os.path.join(directory, dic_file)
	long_names = {}
	if os.path.exists(dic_path):
		with open(dic_path, 'r') as file:
			for line in file:
				parts = line.strip().split(' ')
				long_names[parts[0]] = parts[1]
				# print('[' + parts[0] + '] -> [' + parts[1] + ']')

	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			decrypt_file_or_folder_name(os.path.join(root, name), long_names, password)
		for name in dirs:
			decrypt_file_or_folder_name(os.path.join(root, name), long_names, password)
	# don't delete for debug
	# if os.path.exists(dic_path):
		# os.remove(dic_path)


def encrypt_folder(directory, out_dir, password):
	"""
	encrypt names and data of files and subfolders inside a folder recursively
	and save to a new folder `prefix + directory`
	"""
	encrypt_files_in_folder(directory, out_dir, password)
	encrypt_names_in_folder(out_dir, password)

# decrypt names and data of files and subfolders inside a folder recursively
# and save to a new folder `prefix + directory`
def decrypt_folder(directory, out_dir, password):
	decrypt_files_in_folder(directory, out_dir, password)
	decrypt_names_in_folder(out_dir, password)

# ====== Private Routines ========


def str64_to_strN(base64_str, custom_base_chars):
	"""
	convert a base 64 string to a base N string
	"""
	# Decode the base64 string to bytes
	decoded_bytes = base64.b64decode(base64_str)
	# Convert bytes to integer
	num = int.from_bytes(decoded_bytes, 'big')
	# Convert integer to custom base
	base = len(custom_base_chars)
	if num == 0:
		return custom_base_chars[0]
	result = []
	while num:
		num, rem = divmod(num, base)
		result.append(custom_base_chars[rem])
	return ''.join(reversed(result))


def strN_to_str64(custom_str, custom_base_chars):
	"""
	convert base N string to a base 64 string
	"""
	# Convert custom base string to integer
	base = len(custom_base_chars)
	num = 0
	for char in custom_str:
		num = num * base + custom_base_chars.index(char)
	# Convert integer to bytes
	num_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
	# Encode bytes to base64
	return base64.b64encode(num_bytes).decode()


main()
