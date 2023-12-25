#!/usr/bin/python3

import os
import sys
import subprocess

# encrypt a file
def encrypt(file_to_encrypt, encrypted_file, password):
	command = [
		'openssl', 'aes-256-cbc', '-nosalt', '-pbkdf2',
		'-in', file_to_encrypt,
		'-out', encrypted_file,
		'-pass', 'pass:' + password
	]

	# Run the command
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

	# Run the command
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
	# Run the command
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
	# Run the command
	result = subprocess.run(command, input=string_to_decrypt+'\n', text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode != 0:
		raise RuntimeError('encryption failed!')
	return result.stdout

# encrypt file and subfolder names inside a folder recursively
def encrypt_names_in_folder(directory, password, prefix):
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			os.rename(os.path.join(root, name), os.path.join(root, encrypt_str(name, password)))
		for name in dirs:
			os.rename(os.path.join(root, name), os.path.join(root, encrypt_str(name, password)))

# tests
string_to_decrypt = encrypt_str('需要1232343453456加密的字符串', '我的密码')
print(string_to_decrypt)

decrypted_string = decrypt_str(string_to_decrypt, '我的密码')
print(decrypted_string)


