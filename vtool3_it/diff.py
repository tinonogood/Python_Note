#!/usr/bin/env python3

import sys
import difflib

def diff_context(file, temple, diff):

#    file = sys.argv[0]
#    temple = sys.argv[1]
#    diff = sys.argv[2]

    fn = open(file, "r")
    fo = open(temple, "r")
    
    fileNew = fn.readlines()
    fileOld = fo.readlines()
    
    fn.close()
    fo.close()
    
    outFileDiff = open(diff, "w")
    
    diff = difflib.context_diff(fileNew, fileOld, n=1)
    outFileDiff.write(''.join(diff))

    outFileDiff.close()

#if __name__ == "__main__":
#   diff_context(sys.argv[1],sys.argv[2], sys.argv[3])
