import filecmp
#from nltk.tokenize import word_tokenize
import os
import sys
import hashlib

#print filecmp.cmp('/Users/Ben/Documents/BinaryClone/NorCodeRegion/bzip2_50_1/BZ2_decompress_2429_2.txt', '/Users/Ben/Documents/BinaryClone/NorCodeRegion/bzip2_50_1/BZ2_decompress_2431_3.txt')
def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

total_num=0
def printResults(dict1):
    global total_num
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        #total_num = total_num+len(results)
        print('Clones Found:')
        print('The clones are identical. The name could differ, but the content is identical')
        #f = open ('Sourceline.txt','w')
        os.system("echo '___________________' >> Sourceline.txt")
        os.system("echo '\n' >> Sourceline.txt")
        print('___________________')
        for result in results:
            for subresult in result:
                total_num = total_num + len(result)
                #name = subresult.split("lbm_150-200/")[1].split(".txt")[0]
                #start = int(name.split("_")[-2])
                #print start
                #end = int(name.split("_")[-1])+int(start)
                #print end
                #real_name = name.split('_'+name.split("_")[-2])[0]
                #with open("/home/hongfa/Dropbox/lbm_binary/"+real_name+".txt") as f:
                #    inst=f.readlines()
                #start_addr = '0x'+inst[start].split(":")[0].strip(" ")
                #end_addr = '0x'+inst[end-1].split(":")[0].strip(" ")
                #f.write("start:")
                #os.system("echo 'start:' >> Sourceline.txt")
                #os.system("addr2line -e /home/hongfa/workspace/SPEC2006/CFP2006/lbm/lbm.x86"+" "+start_addr+" >> Sourceline_lbm.txt")
                #os.system("echo '\n' >> Sourceline.txt")
                #f.write("\n")
                #f.write("end:")
                #os.system("echo 'end:' >> Sourceline.txt")
                #os.system("addr2line -e /home/hongfa/workspace/SPEC2006/CFP2006/lbm/lbm.x86"+" "+end_addr+" >> Sourceline_lbm.txt")                                                                                                      ".txt")
                #os.system("echo '\n' >> Sourceline.txt")
                #f.write("\n")
                print('\t\t%s' % subresult)
            print('___________________')
            os.system("echo '___________________' >> Sourceline.txt")
            os.system("echo '\n' >> Sourceline.txt")

    else:
        print('No Identical clones found.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        printResults(dups)
    else:
        print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')

    print ('Total number is %d' %total_num)