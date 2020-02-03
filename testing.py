import sys
import re
from pathlib import Path

ceedlingPath = Path('ws_ceedling')
testrgx = re.compile('^[ ]*[/][*][ ]*[<][ ]*test[ ]*[>][ ]*[*][/].*')
testrwgend = re.compile('^[ ]*[/][*][ ]*[<][ ]*[/]test[ ]*[>][ ]*[*][/].*')

def findFile(filename):
    files = Path('.').rglob(filename)
    srcfile = None
    for f in files:
        if not ceedlingPath in f.parents:
            srcfile = f

    return srcfile

def generateTestSrc(inputfile, outputfile):
    count = 0
    for line in inputfile:

        if testrgx.match(line):
            count = count + 1
        elif testrwgend.match(line):
            outputfile.write(line)
            count = count - 1
        
        if count > 0:
            outputfile.write(line)
            

if (len(sys.argv) != 2):
    print("make test MODULE=<name>")
else:
    module = sys.argv[1]
    c_file = module + ".c"
    h_file = module + ".h"
    print("C {}".format(c_file))
    print("H {}".format(h_file))
    srcfile = findFile(c_file)
    if srcfile:
        print(srcfile)
    
    incfile = findFile(h_file)
    if incfile:
        print(incfile)

    srcbycl = open('ws_ceedling/src/' + c_file, 'w')
    srcfile = open(srcfile, 'r')
    # count = 0
    # for line in srcfile:

    #     if testrgx.match(line):
    #         count = count + 1
    #     elif testrwgend.match(line):
    #         srcbycl.write(line)
    #         count = count - 1
        
    #     if count > 0:
    #         srcbycl.write(line)
    generateTestSrc(srcfile, srcbycl)
 
    incbycl = open('ws_ceedling/src/' + h_file, 'w')
    incfile = open(incfile, 'r')

    generateTestSrc(incfile, incbycl)

    srcbycl.close()
    srcfile.close()