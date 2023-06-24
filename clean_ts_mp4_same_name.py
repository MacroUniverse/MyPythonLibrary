#! /usr/bin/python3
import os
import glob

# Traverse the directory recursively
for ts_file in glob.glob('**/*.ts', recursive=True):
    # Remove .ts extension
    base_name = os.path.splitext(ts_file)[0]
    
    # Add .mp4 extension
    mp4_file = base_name + '.mp4'
    
    # Check if the .mp4 file exists
    if os.path.isfile(mp4_file):
        print(f"Found matching .mp4 file for {ts_file}, deleting .ts file.")
        os.remove(ts_file)
