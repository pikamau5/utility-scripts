# Find files that are set as writable but are not checked out in perforce
# and files that are in the folder but not added to perforce

# Replace these variables with your own info
user = "laura"  # your p4 username here
stream = 'assets'
local_dir = 'W:\\p4\\laura_laura-homepc_assets'
ignore_files = ["*_log_*", "*bak*", "site-packages"]
folders = ["otls", "laura"]

import subprocess
import os
import fnmatch

# Function to normalize file paths for comparison
def normalize_path(path):
    return os.path.normpath(path).lower()

# Function to check if a file should be ignored
def should_ignore(file):
    for pattern in ignore_files:
        if fnmatch.fnmatch(file, pattern):
            return True
    return False

# Function to check if a path is within the specified folders
def is_in_specified_folders(path):
    for folder in folders:
        if folder in path:
            return True
    return False

# List all files in the specified directories, ignoring those that match the ignore patterns
all_files = []
for (parent, _, files) in os.walk(local_dir):
    if is_in_specified_folders(parent):
        for name in files:
            if not should_ignore(name):
                all_files.append(os.path.join(parent, name))

# List writable files
writable_files = [file for file in all_files if os.access(file, os.W_OK)]

# Get p4 files
stream_slash = '//' + stream + '/...'
p4out = subprocess.run(['p4', 'files', stream_slash], stdout=subprocess.PIPE, shell=True, encoding='utf-8', errors='ignore').stdout
p4out = p4out.splitlines()
p4files = []
for line in p4out:
    if 'no such file(s)' in line:
        continue
    line = line.split('#')[0].strip()  # Remove revision info
    winline = line.replace('//' + stream + "/", "")
    winline = os.path.join(local_dir, winline)
    if not should_ignore(winline) and is_in_specified_folders(winline):
        p4files.append(normalize_path(winline))

# Convert lists to sets for faster operations
set_p4files = set(p4files)
set_all_files = set(map(normalize_path, all_files))

# Files that are writable but not checked out
not_checked_out = [file for file in writable_files if normalize_path(file) not in set_p4files]

# Files in folder but not added to perforce
not_in_perforce = [file for file in all_files if normalize_path(file) not in set_p4files]

# Output results
print(f"{len(not_checked_out)} files are writable but not checked out:")
for file in not_checked_out:
    print(file)

print(f"\n{len(not_in_perforce)} files are in the folder but not added to perforce:")
for file in not_in_perforce:
    print(file)