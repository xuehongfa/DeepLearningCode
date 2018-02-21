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

basic_block=getBasicBlock(filename="/home/hongfa/workspace/bzip2_ML/bzip2.txt")

#print basic_block['401e20']

F2= open("/home/hongfa/workspace/bzip2_ML/bzip2_train2.txt", "w")
F3 = open("/home/hongfa/workspace/bzip2_ML/bzip2_label2.txt", "w")
#F4 = open("/home/hongfa/workspace/openssl/trace_number.txt", "w")
trace_number={}
for root, subFolders, files in os.walk('/home/hongfa/workspace/bzip2_ML/train/'):
    #print root
    #for sub in subFolders:
    print root
    if root == '/home/hongfa/workspace/bzip2_ML/train/':
        continue
    number = 0
    label = root.replace('/home/hongfa/workspace/bzip2_ML/train/', '')
    if len(files) <=100:

        for filename in files:
            #
            filename = root+'/'+filename

            #F3.write(lable + ' ')
            #print lable
            with open(filename,"r") as f:
                blocks = f.read().splitlines()

            for i in range(0,len(blocks)):
                #print i
                for j in range(i+1,len(blocks)):
                    for t in range(i,j):
                        temp=blocks[t].replace('0x','')
                        if temp in basic_block.keys() and t!=j-1:
                            F2.write(basic_block[temp]+' ')
                        if t == j-1:
                            F2.write(basic_block[temp]+'\n')
                    F3.write(label + ' ')
                    #F2.write('\n')
                    number+=1
        trace_number[label]=number
    else:
        for filename in files:
            #
            filename = root+'/'+filename
            label=root.replace('/home/hongfa/workspace/bzip2_ML/train/','')
            #F3.write(lable + ' ')
            #print lable
            with open(filename,"r") as f:
                blocks = f.read().splitlines()

            for i in range(0,len(blocks)):

                temp=blocks[i].replace('0x','')
                if temp in basic_block.keys() and i!=len(blocks)-1:
                    F2.write(basic_block[temp]+' ')
                if i == len(blocks)-1:
                    F2.write(basic_block[temp]+'\n' )
            F3.write(label + ' ')
            #F2.write('\n')
            number+=1


        trace_number[label]=number
with open('/home/hongfa/workspace/bzip2_ML/trace_number.txt', 'w') as file:
    file.write(json.dumps(trace_number))
F3.close()
F2.close()
#F4= open("/home/hongfa/Dropbox/bzip2_test.txt", "w")
#F5 = open("/home/hongfa/Dropbox/bzip2_test_lable.txt", "w")

# for root, subFolders, files in os.walk('/home/hongfa/workspace/bzip2_binary/test/'):
#     #print root
#     #for sub in subFolders:
#     print root
#
#     for filename in files:
#         filename = root+'/'+filename
#         lable=root.replace('/home/hongfa/workspace/bzip2_binary/test/','')
#         #F3.write(lable + ' ')
#         #print lable
#         with open(filename,"r") as f:
#             inst = f.read().splitlines()
#         for i in range(0,len(inst)-1):
#             #print i
#             F5.write(lable + ' ')
#             for j in range(i,len(inst)):
#                 temp=inst[j].replace('0x','')
#                 F4.write(basic_block[temp]+' ')
#             F4.write('\n')





