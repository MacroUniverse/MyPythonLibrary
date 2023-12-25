#!/usr/bin/python3

import sys
import subprocess

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
		sys.exit(1)

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
		sys.exit(1)
