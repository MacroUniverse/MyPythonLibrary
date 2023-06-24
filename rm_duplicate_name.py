#! /usr/bin/python3

# search the current folder and subfolders for files with the same names and only keep the latest version of each filename

import os
import collections
from collections import defaultdict

def remove_duplicates_in_dir(root_dir='.'):
    # Create a dictionary where the keys are the filenames and the values are paths.
    files_dict = defaultdict(list)

    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Add the path to the dict
            files_dict[filename].append(os.path.join(dirpath, filename))

    # Go through each file in the dict
    for filename, filepaths in files_dict.items():
        # If there is more than one file with the same name
        if len(filepaths) > 1:
            # Sort the files by modification time
            filepaths.sort(key=os.path.getmtime)
            
            # Remove duplicates, keep the one with the latest modification time
            for filepath in filepaths[:-1]:  # All but the last
                os.remove(filepath)
                print(f'Removed {filepath}')

if __name__ == "__main__":
    remove_duplicates_in_dir()
