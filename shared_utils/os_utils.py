import os
import shutil
import re
import glob
import subprocess

if os.name == 'nt': 
    os_name = 'win'
else: 
    os_name = 'lin'


def make_new_dirs(folders,clean_subdirs=True):
    if isinstance(folders,str): 
        folders = [folders]
    for folder in folders:
        # Also make parent folder 1 level up e.g. making /data/train will also make /data. Used for shared folders. 
        parent_folder = os.path.dirname(folder)
        if not os.path.exists(parent_folder): 
            os.mkdir(parent_folder)
        if clean_subdirs and os.path.exists(folder): 
                delete_directory(folder)
        if not os.path.exists(folder): 
            os.mkdir(folder)


def move_and_merge_dirs(origin_dir_name, target_dir_name):
    contents = glob.glob(os.path.join(origin_dir_name,'*'))
    for content in contents: 
        shutil.move(content,os.path.join(target_dir_name,os.path.basename(content)))
    delete_directory(origin_dir_name)


def natural_sort(dir_list):
    # Function for sorting files/directories/other lists in natural order and not 1, 10, 100, 2, 20... 
    # Add feature - first first or directories first
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(dir_list, key=alphanum_key)


def delete_directory(target_directory): 
    # This module uses OS calls to speed up removal of large numbers of files compared to shutil's rmtree
    if os.path.exists(target_directory): 
        if os_name == 'win': 
            command = 'rmdir /s /q'
        else: 
            command = 'rm -rf'

        error_code = subprocess.check_output(command + ' ' + target_directory,shell=True)
    else: 
        print('Directory to be deleted does not exist: ' + target_directory)


def list_dir(directory,target_type='',mask='*'): 
    contents = glob.glob(os.path.join(directory,mask))
    
    if not isinstance(directory,str) or not isinstance(target_type,str) or not isinstance(mask,str): 
        raise(TypeError('Directory, type, and mask need to be strings.'))

    if not os.path.exists(directory) or not os.path.isdir(directory): 
        raise(OSError('Input directory not valid.'))
        
    # Mask to only return files or folders
    if target_type == 'files': 
        if '.' in mask: 
            contents = [name for name in contents if name.endswith(target_type)]
        else: 
            contents = [name for name in contents if os.path.isfile(name)]
    elif target_type == 'folders': 
        contents = [name for name in contents if os.path.isdir(name)]
    
    contents = [os.path.join(directory,name) for name in contents]
    return natural_sort(contents)