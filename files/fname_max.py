#!/bin/python3
# 从中间截断文件和文件夹名字长度，使 utf-8 编码的总字节数不超过给定值
# 注意CJK 的 UTF-8 编码几乎都是 3 个字节
# 不重命名最外层文件夹

import os
import shutil

# ==== 参数 ====
path = '1_345678901234' # 要处理的文件夹
max_bytes = 142 # 文件名最大字节数（群晖加密盘是 143）
ratio = 2/3 # 删除位置
separator = '::' # 把删除的字符替换为（可为空）
# ==============

# 重命名（截断）一个文件或文件夹
def fname_max1(root, name):
    name_utf8 = name.encode('utf-8')
    if len(name_utf8) < max_bytes:
        print(name)
        return

    Ncut = len(name_utf8) - max_bytes + len(separator)
    start_cut = int(max_bytes * ratio)
    end_cut = start_cut + Ncut
    name_utf8_cut = name_utf8[:start_cut] + separator + name_utf8[end_cut:]

    while True:
        try:
            name_cut = name_utf8_cut.decode('utf-8')
            break
        except UnicodeDecodeError:
            name_utf8_cut = name_utf8[:end_cut] + name_utf8[end_cut+1:]

    src_file = os.path.join(root, name)
    dst_file = os.path.join(root, name_cut)
    print(f"{src_file}\n --> {name_cut}")
    shutil.move(src_file, dst_file)

# 重命名（截断） `folder` 下的所有文件和文件夹，不包含 `folder`
def fname_max(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir in dirs:
            fname_max1(root, dir)
        for file in files:
            fname_max1(root, file)

# ---------------------------------
fname_max(path)
