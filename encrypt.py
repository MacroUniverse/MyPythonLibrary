#!/usr/bin/python3

import os
import sys
import subprocess
import shutil

# encrypt a file
def encrypt(file_to_encrypt, encrypted_file, password):
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

# decrypt a file
def decrypt(file_to_decrypt, decrypted_file, password):
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

# encrypt a string
def encrypt_str(string_to_encrypt, password):
	command = [
		'openssl', 'enc', '-base64', '-e', '-aes-256-cbc', '-nosalt', '-pbkdf2',
		'-pass', 'pass:' + password
	]
	result = subprocess.run(command, input=string_to_encrypt, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode != 0:
		raise RuntimeError('encryption failed!')
	return result.stdout[:-1]

# decrypt a string
def decrypt_str(string_to_decrypt, password):
	command = [
		'openssl', 'enc', '-base64', '-e', '-aes-256-cbc', '-nosalt', '-pbkdf2', '-d',
		'-pass', 'pass:' + password
	]
	result = subprocess.run(command, input=string_to_decrypt+'\n', text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode != 0:
		raise RuntimeError('decryption failed!')
	return result.stdout

# encrypt files in folder to a new folder named 'enc-'
def encrypt_files_in_folder(directory, password):
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			path = os.path.join(root, name)
			root_new = 'enc-' + root
			if not os.path.exists(root_new):
				os.makedirs(root_new)
			encrypt(path, os.path.join(root_new, name), password)

def decrypt_files_in_folder(directory, password):
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			path = os.path.join(root, name)
			if root[:4] == 'enc-':
				root_new = root[4:]
			else:
				root_new = 'dec-' + root
			if not os.path.exists(root_new):
				os.makedirs(root_new)
			decrypt(path, os.path.join(root_new, name), password)

# encrypt names of files and subfolders inside a folder recursively
def encrypt_names_in_folder(directory, password):
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			path_old = os.path.join(root, name)
			name_new = encrypt_str(name, password).replace('/', '-')
			print(path_old, ' -> ', name_new)
			os.rename(path_old, os.path.join(root, name_new))
		for name in dirs:
			path_old = os.path.join(root, name)
			name_new = encrypt_str(name, password).replace('/', '-')
			print(path_old, ' -> ', name_new)
			os.rename(path_old, os.path.join(root, name_new))

# decrypt names of files and subfolders inside a folder recursively
def decrypt_names_in_folder(directory, password):
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			path_old = os.path.join(root, name)
			name_new = decrypt_str(name.replace('-', '/'), password)
			print(path_old, ' -> ', name_new)
			os.rename(path_old, os.path.join(root, name_new))
		for name in dirs:
			path_old = os.path.join(root, name)
			name_new = decrypt_str(name.replace('-', '/'), password)
			print(path_old, ' -> ', name_new)
			os.rename(path_old, os.path.join(root, name_new))

# tests
# string_to_decrypt = encrypt_str('需要1232343453456加密的字符串', '我的密码')
# print(string_to_decrypt)

# decrypted_string = decrypt_str(string_to_decrypt, '我的密码')
# print(decrypted_string)

# encrypt_names_in_folder('test_folder', '我的密码')
# decrypt_names_in_folder('test_folder', '我的密码')

# encrypt_files_in_folder('test_folder', '我的密码')
decrypt_files_in_folder('enc-test_folder', '我的密码')
