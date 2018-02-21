from capstone import *
import glob
import os
import fileinput
# One code region as input
F = open("/home/hongfa/workspace/rnnlm/bzip2.txt", "w")
def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)
for filename in glob.glob("/home/hongfa/Dropbox/openssl/*.txt"):
    #print filename

    with open(filename,"r") as f:
        inst = f.readlines()
    disassemble=''
    inst = [x.strip() for x in inst]
    for ins in inst:
        #print ins
        if len(ins.split("  ")) > 1:
            #print ins
            disassemble = ins.split(":")[1].split('  ')[-1].lstrip()
            #disassemble.replace(",",'')
            if len(disassemble.split(", "))>1:
                dis = disassemble.split(", ")[0]+" "+disassemble.split(", ")[1]
            else:
                dis = disassemble.split(", ")[0]
            F.write(dis+'\n')
        else:
            #print i
            if ins.startswith("0"):
                continue
            else:
                F.write(ins.replace(", ",' ')+'\n')



remove_empty_lines('/home/hongfa/workspace/rnnlm/openssl.txt')







