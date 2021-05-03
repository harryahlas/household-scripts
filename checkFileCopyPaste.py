# -*- coding: utf-8 -*-
"""
Created on Sat May  1 20:19:52 2021

This script is intended for use after files have been copied to a new folder.
Sometimes Windows has an error that gets you can skip over but, as a result,
some files are not copied.
This script looks for files that did not get copied and then copies them over.

@author: Harry Ahlas
"""

import glob
import shutil, os
     
     
# Find files that should have been copied from
dir_from = 'E:\\Android\\media\\'
files_in_dir_from = []

for filename in glob.iglob(dir_from + '**/**', recursive=True):
    filename = filename.replace("E:\\Android\\media\\", "")
    files_in_dir_from.append(filename)

# Find files that were actually copied to
dir_to= 'D:\\android_backups\\external_card_backup_20210501\\Android\\media\\'
  
files_in_dir_to = []
for filename in glob.iglob(dir_to + '**/**', recursive=True):
    filename = filename.replace("D:\\android_backups\\external_card_backup_20210501\\Android\\media\\", "")
    files_in_dir_to.append(filename)
     
# Identify the files that were not copied
missing_files = [x for x in files_in_dir_from if x not in files_in_dir_to]

# Copy missing files
for missing_file in missing_files:
    
    missing_file_from_path = dir_from + missing_file
    missing_file_to_path = dir_to + missing_file
    os.makedirs(os.path.dirname(missing_file_to_path), exist_ok=True) # Create folder if it doesn't exist
    shutil.copy(missing_file_from_path, missing_file_to_path)

shutil.copy('E:\\Android\\media\\Vincent Wojno\\Unknown Album (1-22-2010 9-28-22 AM)\\04 TOT2.wma',
            'C:\\tossfolder\\throw.t')

open("sample.txt", "w").write(str(missing_files))

os.mkdir('C:\\tossfolder\\thro\\')

shutil.copy(src_fpath, dest_fpath)


#copy from alternate folder
# Copy missing files
dir_alt = "D:/Music/"
write_log = []
for missing_file in missing_files[25:89]:
    
    missing_file_alt_path = dir_alt + missing_file
    write_log.append(missing_file_alt_path + " exists? " + str(os.path.exists(missing_file_alt_path)))
    if os.path.exists(missing_file_alt_path):
        print("made it to" + missing_file_alt_path)
        missing_file_to_path = dir_to + missing_file
        os.makedirs(os.path.dirname(missing_file_to_path), exist_ok=True) # Create folder if it doesn't exist
        shutil.copy(missing_file_alt_path, missing_file_to_path)
    else:
        print("skipping" + missing_file_alt_path)
        
