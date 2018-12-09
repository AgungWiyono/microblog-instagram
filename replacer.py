import os
import sys
import fileinput

textToSearch = "kwargs['message']"
textToReplace = "kwargs['msg']"

fileToSearch = '/usr/local/lib/python3.6/site-packages/flask_restplus/errors.py'

with open(fileToSearch) as f:
    s = f.read()
    if textToSearch not in f:
        print('No Change needed.')
    else:
        print("Let's do our job.")

with open(fileToSearch, 'w') as f:
    new_line = s.replace(textToSearch, textToReplace)
    f.write(new_line)

print('Goodbye')
