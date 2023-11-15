# Find files that are set as writable but are not checked out in perforce

# Replace these variables with your own info
user = "user" # your p4 username here
stream = 'stream/main'
local_dir = 'C:\path-to-stream-dir'

import subprocess
import os
import glob

allFiles = []

files = [
       os.path.join(parent, name)
       for (parent, subdirs, files) in os.walk(local_dir)
       for name in files + subdirs
   ]


writable_files = []
for file in files:
    if os.path.isdir(file):
        continue
    if os.access(file, os.W_OK):
        writable_files.append(file)


# get p4 files
stream_slash = '//' + stream + '/...'
p4out = subprocess.run(['p4', 'opened', '-u', user, '-s', stream_slash], stdout=subprocess.PIPE, shell=True,
                       encoding='utf-8', errors='ignore').stdout
p4out = p4out.splitlines()
p4files = []
for line in p4out:
    line = line.split(" - ")[0]
    # print(line)
    winline = line.replace('//' + stream + "/", "")
    winline = local_dir + "/" + winline
    p4files.append(winline)


asdf = []
for file in writable_files:
    if file not in p4files:
        asdf.append(file)

print ("{} files are writable but not checked out:".format(len(asdf)))
for file in asdf:
    print(file)