from capstone import *
import glob


# One code region as input
CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
md = Cs(CS_ARCH_X86, CS_MODE_64)
OPTYPE = ["MEM", "REG", "VAL"]
Window = 160
Stride = 2
# A list of register names
REG = ["%rax","%rcx","%rdx","%rbx","%rsp","%rbp","%rsi","%rdi","%eax","%ecx","%edx","%ebx","%esp","%ebp","%esi","%edi","%r*"]
N = []
minT = 150
Static_ins = 0
for filename in glob.glob("/home/hongfa/Dropbox/sphinx3_binary/*.txt"):
    func = filename.split("/home/hongfa/Dropbox/sphinx3_binary")[1].split(".txt")[0]
    with open(filename,"r") as f:
        inst = f.readlines()
    inst = [x.strip() for x in inst]
    Static_ins =Static_ins + len(inst)
    print filename
    inst_region = []
    w = 1
    line = 0
    offset = 0
    start = 0
    while start <len(inst) :
        for i in range(minT,minT+Window+1):
            #Token = minT
            #while (w+Token)<len(inst):
            #print len(inst)
            if (start+i) > len(inst):
                break
            inst_region = inst[start:start+i]

            #print inst[w]
            #StartAddress = inst[w].split("	")[0].split(":")[0]
            F = open("/home/hongfa/workspace/NorCodeRegion/sphinx3_150-200/"+func+"_"+str(start)+"_"+str(i)+".txt","w")
            for ins in inst_region:

                # if ins == inst[0]:
                # continue
                # print i
                # address = i.split("	")[1].split("	")[0]
                if len(ins.split("	")) == 3:
                    mnemonic = ins.split("	")[2].split("   ")[0]
                    if mnemonic.find(" ") != -1:
                        mnemonic = mnemonic.split(" ")[0].strip(" ")
                        # print mnemonic
                else:
                    if len(ins.split(":")) == 2:

                        F.write("null\n")
                        continue
                    else:
                        continue

                op_str = ins.split(mnemonic)[1].strip(" ")
                # print op_str
                # else:
                # op_str = "null"

                # print("0x%s:\t%s\t%s" %(address, mnemonic, op_str))
                idx = 0
                oprand = str(op_str)
                Nor_op = ""
                op_list = []
                # print oprand
                # oprand = oprand.strip(" ")
                if oprand.find("#") != -1:
                    oprand = oprand.split(" ")[0].strip(" ")
                # if oprand == :
                #print oprand

                if "," in oprand:
                    if len(oprand.split(",")) == 2:

                        op_list = oprand.split(",", 1)
                    else:
                        if oprand.split(",", 1)[1].find(")") != -1:
                            op_list.append(oprand)

                else:
                    op_list.append(oprand)
                for o in op_list:
                    # print o
                    if o in REG or o.startswith("%"):
                        t = OPTYPE[1]
                    else:
                        # print o
                        if (o.find("(") != -1) and (o.find("x") != -1) :
                            t = OPTYPE[2]
                        else:
                            if (o.find("<") != -1):
                                # print o
                                t = OPTYPE[0]
                            else:
                                t = OPTYPE[2]

                    # if o not in N:
                    #     idx = len(N)
                    #     N.append(o)
                    #
                    # else:
                    #     idx = N.index(o)

                    Nor_o = t
                    Nor_op = Nor_op + " " + Nor_o

                Nor_i = str(mnemonic) + " " + Nor_op
                # print Nor_i
                F.write(Nor_i + "\n")

                #Token = Token + Stride

        start = start+Stride

#print w
print Static_ins




