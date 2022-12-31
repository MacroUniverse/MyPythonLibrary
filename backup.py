# === params ===
src = '/home/addis/Desktop/py-backup-test (copy)/source-drive'
dest = '/home/addis/Desktop/py-backup-test (copy)/backup-drive'
ver = '2'
# ==============

import os
import sys
# import hashlib # for sha1sum
import subprocess # for calling shell command
import shutil # for copy file
import natsort # natural sort folder name

# pipe won't work!
def shell_cmd(*cmd):
    process = subprocess.Popen(list(cmd), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error != None:
        print(error)
        sys.exit(1)
    return output.decode()

# hash every file in current directory and sort to a list
# write to file if fname provided
def sha1_cwd(fname=None):
    output = shell_cmd('find', '.', '-type', 'f', '-exec', 'sha1sum', '{}', ';').splitlines();
    output.sort()
    if fname != None:
        f = open('sha1sum.txt', 'w')
        f.write('\n'.join(output))
        f.close()
    return output

# return True if cwd has changed based on sha1sum.txt, then write sha1sum-new.txt
def hash_or_rehash_cwd(no_rehash=False):
    if os.path.exists('sha1sum-new.txt'):
        return True
    if not os.path.exists('sha1sum.txt'):
        print('sha1sum.txt or sha1sum-new.txt not found, hasing...')
        sha1_cwd('sha1sum.txt')
        return False
    elif no_rehash: # sha1sum.txt exist
        print("sha1sum.txt exist! [no_rehash] assuming it's up to date")
    else: # sha1sum.txt exist
        print('sha1sum.txt exist! rehashing...')
        sha1_new = sha1_cwd();
        # delete sha1sum.txt itself
        for i in range(len(sha1_new)):
            if sha1_new[i][44:] == 'sha1sum.txt':
                del sha1_new[i]
                break
        sha1_new = '\n'.join(sha1_new);
        f = open('sha1sum.txt', 'r')
        sha1 = f.read();
        f.close()
        if sha1_new != sha1:
            f = open('sha1sum-new.txt', 'w')
            f.write(sha1_new)
            f.close()
            print('sha1sum.txt changed, compare to sha1sum-new.txt manually!')
            return True
        else:
            print('no change or corruption!');
            return False

os.chdir(src)

amend_run = os.path.exists('backup.py_has_conflict_waiting_amend_run')
if amend_run:
    print('running in amend mode!'); print('')
    os.remove('backup.py_has_conflict_waiting_amend_run')
    
need_review = False;

# === loop through all sub folders ===
folders = next(os.walk('.'))[1];
for folder in folders:
    print(''); print('='*40)
    print(folder)
    print('='*40); print('')
    folder_ver = folder + '.v' + ver;
    dest1 = dest + '/' + folder + '.sync'
    dest2 = dest1 + '/' + folder_ver
    
    # === check latest backup ===
    dest2_last = ''
    if os.path.exists(dest1):
        backups = next(os.walk(dest1))[1]
        if backups:
            backups = natsort.natsorted(backups)
            folder_ver_last = backups[-1]
            dest2_last = dest1 + '/' + folder_ver_last
            print('found previous backup [' + folder_ver_last + ']')
            print('')

    # === check source folder ===
    print('checking', '['+folder+']'); print('-'*40)
    os.chdir(src + '/' + folder)
    if (hash_or_rehash_cwd(amend_run)): # has change
        print('please review sha1sum-new.txt and replace sha1sum.txt if everything is ok, then run again!')
        print('')
        need_review = True
        continue
    elif not amend_run and dest2_last and (dest2 != dest2_last):
        print('renaming [{}] to [{}]...'.format(folder_ver_last, folder_ver))
        print('-'*40)
        f = open(dest2_last + '/sha1sum.txt', 'r')
        sha1_dest = f.read(); f.close()
        f = open(src + '/' + folder + '/sha1sum.txt', 'r')
        sha1 = f.read(); f.close()
        if (sha1_dest != sha1):
            print('sha1sum.txt differs! this is unexpected!')
            sys.error(1)
        os.rename(dest2_last, dest2)
        print('')
    else:
        print('')

    # === check backup folder (if exist) ===
    if os.path.exists(dest2):
        os.chdir(dest2)
        print('checking ['+folder_ver+']'); print('-'*40)
        if hash_or_rehash_cwd():
            print('================> backup corrupted!!!')
        f = open(dest2 + '/sha1sum.txt', 'r')
        sha1_dest = f.read(); f.close()
        f = open(src + '/' + folder + '/sha1sum.txt', 'r')
        sha1 = f.read(); f.close()
        if (sha1_dest != sha1):
            print('sha1sum.txt differs from source! please use a new version number and run again.')
            open(src + '/backup.py_has_conflict_waiting_amend_run', 'w').close()
            sys.exit(1)
        print('sha1sum.txt maches!'); print('')
        continue
    
    # === do backup ===

    # --- direct copy ---
    if dest2_last == '':
        print('---- no previous backup, copying... ----')
        os.chdir(src)
        os.makedirs(dest2)
        print(shell_cmd('cp', '-av', folder + '/.', dest2));
        print('');
        continue

    # --- delta sync ---
    print('---- checking previous backup [' + os.path.split(dest2_last)[1] + '] ----')    
    os.chdir(dest2_last)
    if (hash_or_rehash_cwd()):
        print('================> backup corrupted!!!')
        continue

    print('---- starting delta sync ----')
    f = open('sha1sum.txt', 'r')
    sha1_last = f.read().splitlines()
    f.close()
    os.chdir(src + '/' + folder)
    f = open('sha1sum.txt', 'r')
    sha1 = f.read().splitlines()
    f.close()
    
    for i in range(len(sha1)):
        hash = sha1[i][:40]
        path = sha1[i][43:]
        # ensure dest path exist
        tmp = os.path.split(dest2+path)[0]
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        # try to match a previous backup file
        match = False
        for j in range(len(sha1_last)):
            if sha1_last[j][:40] == hash:
                path_last = sha1_last[j][43:]
                os.rename(dest2_last+path_last, dest2+path)
                del sha1_last[j]
                match = True
                break
        if not match:
            shutil.copyfile(path[1:], dest2+path)
    
    shutil.copyfile('sha1sum.txt', dest2 + '/' + 'sha1sum.txt')
    f = open(dest2_last+'/sha1sum.txt', 'w')
    f.write('\n'.join(sha1_last))
    f.close()
    print('')
    
    
    print('------- debug: rehash backup folder ------')
    os.chdir(dest2)
    hash_or_rehash_cwd()

if need_review:
    print('============ review & rerun needed =============')
    open(src + '/backup.py_has_conflict_waiting_amend_run', 'w').close()
else:
    print('=============== ALL DONE ===============')
