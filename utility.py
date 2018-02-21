from capstone import *
import glob
basic_block={}
import os
import json

def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)
remove_empty_lines('/home/hongfa/workspace/bzip2_ML/bzip2_train.txt')