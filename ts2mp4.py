#! /usr/bin/python3
import os
import subprocess

# Current directory
dir_path = os.getcwd()

# Extension to look for
extension = ".ts"

# Check for the type of operating system
is_windows = os.name == 'nt'

for dirpath, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(extension):
            print("\n\n\n===============", file, "=================")
            full_file_path = os.path.join(dirpath, file)
            output_file_path = os.path.splitext(full_file_path)[0] + '.mp4'
            
            # FFmpeg command
            command = ['ffmpeg', '-y', '-i', full_file_path, '-c', 'copy', output_file_path]
            
            # Run the command and check for errors
            try:
                subprocess.run(command, shell=is_windows, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while processing file {full_file_path}")
                print(f"Error message: {str(e)}")
