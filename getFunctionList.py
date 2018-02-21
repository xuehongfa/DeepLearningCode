from capstone import *
import glob
basic_block={}
import os


F= open("/home/hongfa/workspace/bzip2_ML/function_list.txt", "w")
def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)
# One code region as input



def getFunctionList(filename):
    remove_empty_lines(filename)
    basic_block=[]
    with open(filename,"r") as f:
        inst = f.read().splitlines()
    disassemble=''
    ins_key = ''
    #inst = [x.strip() for x in inst]
    for i in range (0,len(inst)):

        #print ins
        basic_trace = ''

        if len(inst[i].split(": "))==2 and '<'in inst[i]:
            function_name= inst[i].split('<')[1].split('>')[0]
            function_address = inst[i].split(':')[0].replace('0000000000','')
            F.write(function_name+':'+function_address+'\n')




getFunctionList(filename="/home/hongfa/workspace/bzip2_ML/bzip2.txt")