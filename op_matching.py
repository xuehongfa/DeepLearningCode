from __future__ import division
import glob
basic_block={}
import os
import numpy as np

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

def getBasicBlock(filename):
    remove_empty_lines(filename)

    with open(filename,"r") as f:
        inst = f.read().splitlines()
    disassemble=''
    ins_key = ''
    #inst = [x.strip() for x in inst]
    for i in range (0,len(inst)):

        #print ins
        basic_trace = ''

        if len(inst[i].split(": "))==1:
            #print inst[i]


            if inst[i].startswith('0000000000'):
                temp=inst[i].replace('0000000000','').replace(':','')
                ins_key = temp
                #print ins_key

                j=i+1
                while len(inst[j].split(": "))!=1 and j <len(inst)-1:
                    #print inst[j]
                    if len(inst[j].split("  ")) > 1:
                        disassemble = inst[j].split(":")[1].split('  ')[-1].lstrip()
                        # disassemble.replace(",",'')
                        if len(disassemble.split(", ")) > 1:
                            dis = disassemble.split(", ")[0] + " " + disassemble.split(", ")[1]
                        else:
                            dis = disassemble.split(", ")[0]
                        basic_trace=basic_trace+dis+" "

                    j+=1
                #print basic_trace
                basic_block[temp]=basic_trace

            else:
                #print inst[i]
                tem_ins=inst[i].lstrip()
                basic_block[ins_key] = basic_block[ins_key]+' '+tem_ins
                    #print tem_ins
    return basic_block

#basic_block=getBasicBlock(filename="/home/hongfa/workspace/rnnlm/openssl.txt")


#print basic_block['401e20']




def getTrainingLabel(filename):
    with open(filename, "r") as f:
        train_label = f.readline()

    t = np.fromstring(train_label, dtype=int, sep=' ')
    t = np.array(t)
    return t


with open("/home/hongfa/Dropbox/thttpd_train2.txt", "r") as f3:
    train = f3.readlines()
train = [x.strip() for x in train]
with open("/home/hongfa/Dropbox/thttpd_label2.txt", "r") as f4:
    label = f4.readline()
label=label.split()

#print label

print len(label)
print len(train)

