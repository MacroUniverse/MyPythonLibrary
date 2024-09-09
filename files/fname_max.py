#!/bin/python3
# 从中间截断文件和文件夹名字长度，使 utf-8 编码的总字节数不超过给定值
# 注意CJK 的 UTF-8 编码几乎都是 3 个字节
# 不重命名最外层文件夹

import os
import shutil

# ==== 参数 ====
path = '.' # 要处理的文件夹
is_dry = True # 只打印不真正重命名
max_bytes = 140 # 文件名最大字节数（群晖加密盘是 143）
ratio = 2/3 # 删除位置
separator = '::' # 把删除的字符替换为（可为空）
ignore_dirs = {'.git'}
# ==============

# 重命名（截断）一个文件或文件夹
def fname_max1(root, name):
    name_utf8 = name.encode('utf-8')
    if len(name_utf8) <= max_bytes:
        return

    sep_utf8 = separator.encode('utf-8')
    N_cut_byte = len(name_utf8) - max_bytes + len(sep_utf8) # 需要删除的字节数
    
    Nbyte = 0
    start0_utf8 = int(max_bytes * ratio) # name 开头至少要保留的子节数
    for i in range(1, len(name)):
        Nbyte += len(name[i].encode('utf-8'))
        if Nbyte >= start0_utf8:
            break
    else:
        raise Exception('unkown')

    i += 1
    start = i # 删除 name[start:end]
    start_utf8 = Nbyte # 实际上 name 开头保留的字节数
    end0_bytes = start_utf8 + N_cut_byte
    
    for i in range(i, len(name)):
        Nbyte += len(name[i].encode('utf-8'))
        if Nbyte >= end0_bytes:
            break
    else:
        raise Exception('unkown')

    end = i + 1 # 删除 name[start:end], 即 name_utf8[start_utf8:Nbyte]
    name_cut = name[:start] + separator + name[end:]
    name_cut_utf8 = name_cut.encode('utf-8')
    if len(name_cut_utf8) > max_bytes:
        raise Exception('unexpected: len(name_cut_utf8) = ' + str(len(name_cut_utf8)))

    src_file = os.path.join(root, name)
    dst_file = os.path.join(root, name_cut)
    print(root)
    print(f'   {name}')
    print(f' > {name_cut}')
    print('---------------------------')
    if not is_dry:
        shutil.move(src_file, dst_file)

# 重命名（截断） `folder` 下的所有文件和文件夹，不包含 `folder`
def fname_max(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        rel_root = os.path.relpath(root, folder)
        rel_root_prts = os.path.normpath(rel_root).split(os.sep)
        ignr = False
        for ign_dir in ignore_dirs:
            if ign_dir in rel_root_prts:
                ignr = True; break
        if ignr:
            continue
        for dir in dirs:
            fname_max1(root, dir)
        for file in files:
            fname_max1(root, file)

# ---------------------------------
fname_max(path)
