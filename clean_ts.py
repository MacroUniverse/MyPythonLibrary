#! /usr/bin/python3

import os
import shutil

def delete_ts_files():
    current_dir = os.getcwd()
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.mkv'):
                print(file)
                ts_file_path = os.path.join(root, file)
                mp4_file_path = os.path.join(root, file[:-4] + '.mp4')
                print(mp4_file_path)
                if os.path.exists(mp4_file_path):
                    os.remove(ts_file_path)
                    print(f'Deleted {ts_file_path}')
                    print('')
                    
delete_ts_files()
