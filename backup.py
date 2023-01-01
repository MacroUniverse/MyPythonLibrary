#! /usr/bin/python3

# a very simple incremental backup utility
# every subfolder `folder` in `src` will be backed up to `dest/folder.sync/folder.v???`
# where `???` is version number `ver`
# incremental backup will just move identical files from previous version, if any exist
# each folder will have `sha1sum.txt` keeping the hash for every file inside
# just follow the instructions for other cases ...
# you can manually generate sha1sum.txt with `find . -type f -exec sha1sum {} \; | sort > sha1sum-new.txt`

# === params ===========================
src = '/mnt/d/'
dest = '/mnt/q/'
ver = '0'
select = [] # only backup these sub-dirs
start = '电影' # skip until this folder
ignore = ['数学物理考研试卷']
# =====================================

import os
import sys
import hashlib # for sha1sum
import subprocess # for calling shell command
import shutil # for copy file
import errno
import natsort # natural sort folder name

# copy folder recursively
def copy_folder(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            # raise
            print('copy_folder() failed! you might not have permission!')
            exit(1)

# hash every file in current directory and sort hash to a list
# sha1_cwd('sha1sum.txt') should be the same with `find . -type f -exec sha1sum {} \; | sort > sha1sum.txt`
# write to file if fname provided
# doesn't include `fname` itself
def sha1_cwd(fname=None, exclude={'sha1sum.txt', 'sha1sum-new.txt', 'sha1sum-diff.txt'}):
    flist = file_list_r('./')
    sha1 = []
    Nf = len(flist)
    if fname != None:
        exclude.add(fname)
        for i in range(Nf):
            f = flist[i]
            line = sha1file(f) + '  ' + f
            print('[{}/{}] {}    ||||||||||||||\r'.format(i+1, Nf, line[44:]), end="", flush=True)
            if os.path.split(f)[1] in exclude:
                continue
            sha1.append(line)
        sha1.sort()
        f = open(fname, 'w')
        f.write('\n'.join(sha1) + '\n')
        f.close()
    else: # fname == None
        for i in range(Nf):
            f = flist[i]
            line = sha1file(f) + '  ' + f
            print('[{}/{}] {}    ||||||||||||||\r'.format(i+1, Nf, line[44:]), end="", flush=True)
            if os.path.split(f)[1] in exclude:
                continue
            sha1.append(line)
        sha1.sort()
    print('', flush=True)
    return sha1

# return True if cwd has changed based on sha1sum.txt, then write sha1sum-new.txt
# if sha1sum.txt is empty, will update automatically, and return False
def hash_or_rehash_cwd(no_rehash=False):
    if os.path.exists('sha1sum-new.txt'):
        return True
    if not os.path.exists('sha1sum.txt'):
        print('sha1sum.txt or sha1sum-new.txt not found, hasing...', flush=True)
        sha1_cwd('sha1sum.txt')
        return False
    elif no_rehash: # sha1sum.txt exist
        print("sha1sum.txt exist! [no_rehash] assuming it's up to date", flush=True)
    else: # sha1sum.txt exist
        print('sha1sum.txt exist! rehashing...', flush=True)
        sha1_new = sha1_cwd()
        sha1_new = '\n'.join(sha1_new) + '\n'
        f = open('sha1sum.txt', 'r')
        sha1 = f.read()
        f.close()
        if os.stat('sha1sum.txt').st_size == 0: # sha1sum.txt is empty
            print('sha1sum.txt is empty, update automatically...', flush=True)
            f = open('sha1sum.txt', 'w')
            f.write(sha1_new); f.close()
            return False
        elif sha1_new != sha1:
            f = open('sha1sum-new.txt', 'w')
            f.write(sha1_new)
            f.close()
            print('sha1sum.txt changed, compare to sha1sum-new.txt manually!', flush=True)
            return True
        else:
            print('no change or corruption!', flush=True)
            return False

# show difference between sha1sum-new.txt and sha1sum.txt of current folder
def diff_cwd():
    f = open('sha1sum.txt', 'r')
    sha1 = f.read().splitlines(); f.close()
    f = open('sha1sum-new.txt', 'r')
    sha1_new = f.read().splitlines(); f.close()
    i = 0; j = 0
    output = []
    while 1:
        if i == len(sha1):
            for j in range(j, len(sha1_new)):
                output.append(sha1_new[j][44:] + ' [new]')
            break
        elif j == len(sha1_new):
            for i in range(i, len(sha1)):
                output.append(sha1[i][44:] + ' [deleted]')
            break
        hash = int(sha1[i][:40], 16)
        hash_new = int(sha1_new[j][:40], 16)
        if hash == hash_new:
            i += 1; j += 1
        elif hash < hash_new:
            output.append(sha1[i][44:] + ' [deleted]')
            i += 1
        else: # hash_new < hash
            output.append(sha1_new[j][44:] + ' [new]')
            j += 1
    output.sort()
    return ('\n'.join(output))

# sha1sum of a file
# use 1MiB buffer size fot big file
def sha1file(fname, buff_sz=1024*1024):
    if os.path.getsize(fname) <= buff_sz:
        f = open(fname, 'rb')
        data = f.read()
        sha1 = hashlib.sha1(data)
    else:
        sha1 = hashlib.sha1()
        with open(fname, 'rb') as f:
            while True:
                data = f.read(buff_sz)
                if not data:
                    break
                sha1.update(data)
    return sha1.hexdigest()

# retur a list all file paths recursively
# paths start with `path` (relative or absolute)
def file_list_r(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files

# remove empty folders recursively
def rm_empty_folders(path, removeRoot=True):
    'Function to remove empty folders'
    if not os.path.isdir(path):
        return
    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                rm_empty_folders(fullpath)
    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        # print("Removing empty folder:", path)
        os.rmdir(path)


## =========== main program ==============

os.chdir(src)

amend_run = os.path.exists('backup.py_has_conflict_waiting_amend_run')
if amend_run:
    print('running in amend mode!'); print('', flush=True)
    os.remove('backup.py_has_conflict_waiting_amend_run')

# recycled code
'''
# pipe won't work!
def shell_cmd(*cmd):
    process = subprocess.Popen(list(cmd), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error != None:
        print(error)
        sys.exit(1)
    return output.decode()
'''

'''
# sha1_cwd() using bash command
def sha1_cwd_bash(fname=None, exclude={'sha1sum.txt', 'sha1sum-new.txt', 'sha1sum-diff.txt'}):
    print('deprecated! use sha1_cwd instead!'); sys.exit(1)
    lines = shell_cmd('find', '.', '-type', 'f', '-exec', 'sha1sum', '{}', ';').splitlines()
    lines.sort()
    if fname != None:
        exclude.add(fname)
    i = 0
    while i < len(lines):
        if os.path.split(lines)[1] in exclude:
            del lines[i]
            i -= 1
        i += 1
    if fname != None:
        f = open('sha1sum.txt', 'w')
        f.write('\n'.join(lines))
        f.close()
    return lines
'''

# === loop through all sub folders ===

os.chdir(src)

if select:
    folders = select
else:
    folders = next(os.walk('.'))[1]
    folders.sort()

# get folders with sha1sum.txt inside
print('folders to backup:'); print(''); i = 0
while i < len(folders):
    folder = folders[i]
    if os.path.exists(folder + '/sha1sum.txt'):
        print('[{}] {}'.format(i+1, folder))
        i += 1
    else:
        del folders[i]
print(''); print('')
Nfolder = len(folders)

# skip until folder = start
ind0 = 0
if start:
    for ind0 in range(Nfolder):
        if folders[ind0] == start:
            break

for ind in range(ind0, Nfolder):
    os.chdir(src)
    folder = folders[ind]

    print(''); print('='*40)
    print('[{}/{}] {}'.format(ind+1, Nfolder, folder))
    print('='*40); print('', flush=True)

    if folder in ignore:
        print('folder ignored by `ignore` param.')
        continue

    folder_ver = folder + '.v' + ver
    dest1 = dest + '/' + folder + '.sync'
    dest2 = dest1 + '/' + folder_ver
    
    # === check latest backup ===
    print('current backup [{}]'.format(folder_ver), flush=True)
    dest2_last = ''
    if os.path.exists(dest1):
        backups = next(os.walk(dest1))[1]
        if backups: # found previous packup(s)
            backups = natsort.natsorted(backups)
            folder_ver_last = backups[-1]
            dest2_last = dest1 + '/' + folder_ver_last
            print('previous backup [{}]'.format(folder_ver_last))
        else: # no previous packup(s)
            print('previous backup not found!')
        print('', flush=True)

    # === check source folder ===
    print('checking', '['+folder+']'); print('-'*40, flush=True)
    os.chdir(src + '/' + folder)

    if (hash_or_rehash_cwd(amend_run)):
        # `folder` has change or corruption
        print('please review changes in [sha1sum-diff.txt] then replace sha1sum.txt with sha1sum-new.txt', flush=True)
        open(src + '/backup.py_has_conflict_waiting_amend_run', 'w').close()
        f = open('sha1sum-diff.txt', 'w')
        f.write(diff_cwd()); f.close()
        continue
    elif not amend_run and dest2_last and (dest2 != dest2_last):
        # `folder` has no change or corruption
        print('can we can renaming [{}] to [{}] ?'.format(folder_ver_last, folder_ver))
        print('-'*40, flush=True)
        f = open(dest2_last + '/sha1sum.txt', 'r')
        sha1_dest = f.read(); f.close()
        f = open(src + '/' + folder + '/sha1sum.txt', 'r')
        sha1 = f.read(); f.close()
        if (sha1_dest != sha1):
            print('sha1sum.txt differs, cannot rename!'); print('', flush=True)
        else:
            os.rename(dest2_last, dest2)
            print('', flush=True)
    else:
        print('', flush=True)

    # === check backup folder (if exist) ===
    if os.path.exists(dest2):
        os.chdir(dest2)
        print('checking ['+folder_ver+']'); print('-'*40, flush=True)
        if not os.path.exists('sha1sum.txt'):
            print('sha1sum.txt not found, unfinished backup?')
            hash_or_rehash_cwd()
        elif hash_or_rehash_cwd():
            print('corrupted backup files?')
            f = open('sha1sum-diff.txt', 'w')
            f.write(diff_cwd()); f.close()
            print('', flush=True)
            continue

        # check sha1sum.txt between src and dest2
        f = open(dest2 + '/sha1sum.txt', 'r')
        sha1_dest = f.read(); f.close()
        f = open(src + '/' + folder + '/sha1sum.txt', 'r')
        sha1 = f.read(); f.close()
        if (sha1_dest != sha1):
            print('='*40)
            print('sha1sum.txt differs from source! please use a new version number and run again.')
            open(src + '/backup.py_has_conflict_waiting_amend_run', 'w').close()
            continue
        print('both sha1sum.txt maches!'); print('', flush=True)
        continue
    
    # === backup folder doesn't exist, backup ===

    # --- no previous backup, direct copy ---
    if dest2_last == '':
        print('---- no previous backup, copying... ----', flush=True)
        os.chdir(src)
        # os.makedirs(dest2)
        # shell_cmd('cp', '-a', folder + '/.', dest2)
        copy_folder(folder, dest2)
        print('', flush=True)
        continue

    # --- delta sync ---
    print('---- checking previous backup [' + os.path.split(dest2_last)[1] + '] ----', flush=True)    
    os.chdir(dest2_last)
    if (hash_or_rehash_cwd()):
        print('================> backup corrupted! should not happen!')
        print('TODO: show the change!'); print('', flush=True)
        continue
    print('')

    print('---- starting delta sync ----', flush=True)
    f = open('sha1sum.txt', 'r')
    sha1_last = f.read().splitlines()
    f.close()
    os.chdir(src + '/' + folder)
    f = open('sha1sum.txt', 'r')
    sha1 = f.read().splitlines()
    f.close()
    rename_count = 0; i = j = 0
    # assuming both sha1_last and sha1 and sorted
    for i in range(len(sha1)):
        hash = sha1[i][:40]
        path = sha1[i][43:]
        # ensure dest path exist
        tmp = os.path.split(dest2+path)[0]
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        # try to match a previous backup file
        match = False
        while j < len(sha1_last):
            hash_last = sha1_last[j][:40]
            if hash_last > hash:
                break
            elif hash_last == hash:
                path_last = sha1_last[j][43:]
                os.rename(dest2_last+path_last, dest2+path)
                rename_count += 1; match = True
                del sha1_last[j]
                break
            j += 1
        if not match: # no match, just copy
            shutil.copyfile(path[1:], dest2+path)
    
    # update previous sha1sum.txt
    shutil.copyfile('sha1sum.txt', dest2 + '/' + 'sha1sum.txt')
    f = open(dest2_last+'/sha1sum.txt', 'w')
    f.write('\n'.join(sha1_last))
    f.close()
    
    # delete empty folders
    # shell_cmd('find', dest2_last, '-empty', '-type', 'd', '-delete')
    rm_empty_folders(dest2_last, False)
    
    print('total files:', len(sha1))
    print('moved from previous version:', rename_count)
    print('', flush=True)
    
    print('------- DEBUG: rehash backup folder ------')
    os.chdir(dest2)
    hash_or_rehash_cwd(); print('', flush=True)

if os.path.exists(src + '/backup.py_has_conflict_waiting_amend_run'):
    print('============ review & rerun needed =============')
else:
    print('=============== ALL DONE ===============')
