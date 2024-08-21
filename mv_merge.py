# merge two folders just like windows
# skip files in conflict, nothing will be lost

import os
import shutil

def merge_folders(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        dst_dir = os.path.join(dst, relative_path)

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_dir, file)

            if os.path.exists(dst_file):
                print(f"Skipping file due to conflict: {dst_file}")
                continue
            print(f"{src_file} -> {dst_file}")
            shutil.move(src_file, dst_file)

# Example usage:
src_folder = "/volume1/data/pljj"
dst_folder = "pljj/"

merge_folders(src_folder, dst_folder)
