# 截断文件和文件夹名字长度，以符合群晖命名规则
import os
import shutil

# 文件名最大字节数
# CJK 的 UTF-8 编码几乎都是 3 个字节
max_bytes = 130

# 重命名（截断）一个文件或文件夹
def fname_max1(root, name):
    name_utf8 = name.encode('utf-8')
    if len(name_utf8) < max_bytes:
        return
    
    name_utf8_cut = name_utf8[:max_bytes]

    while True:
        try:
            name_cut = name_utf8_cut.decode('utf-8')
            break
        except UnicodeDecodeError:
            name_utf8_cut = name_utf8_cut[:-1]
    
    src_file = os.path.join(root, name)
    dst_file = os.path.join(root, name_cut)
    print(f"{src_file} -> {name_cut}")
    shutil.move(src_file, dst_file)

# 重命名（截断） `folder` 下的所有文件和文件夹，不包含 `folder`
def fname_max(folder):
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            fname_max1(root, dir)
        for file in files:
            fname_max1(root, file)

# ---------------------------------
fname_max('./')
