#!/usr/bin/env python
import shutil
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

files_to_delete = (
    '.Python',
    '.installed.cfg'
)

directories_to_delete = (
    'lib', 
    'eggs',
    'parts',
    'develop-eggs',
    'include',
    'downloads',
    'build', 
    'man',
    'share',
    # Win32 only
    'Scripts'
)

ignore_bin_files = (
    '.svn',
    'bootstrap.py',
    'create-bootstrap.py',
    'clean.py'
)

# Delete symlink for virtualenv
for file_to_delete in files_to_delete:
    try:
        os.remove(os.path.join(PROJECT_DIR, file_to_delete))
    except Exception, e:
        print e
        
# Delete all generated files in the bin directory
for file_to_delete in os.listdir(os.path.join(PROJECT_DIR, 'bin')):
    if file_to_delete not in ignore_bin_files:
        try:
            os.remove(os.path.join(PROJECT_DIR, 'bin', file_to_delete))
        except Exception, e:
            print e

# Delete all other directories
for directory_to_delete in directories_to_delete:
    try:
        shutil.rmtree(os.path.join(PROJECT_DIR, directory_to_delete))
    except Exception, e:
        print e
