#!/usr/bin/env python3

#version 0
#compare context & show different with old one

import sys
import difflib

##verify inputs
#USAGE='''
#%s file1 file2 output1 
#'''% __file__
#
#if len(sys.argv)<4:
#        print USAGE
#        sys.exit(2)

#Find Diff
fn = open(sys.argv[1], "r")
fo = open(sys.argv[2], "r")

fileNew = fn.readlines()
fileOld = fo.readlines()

fn.close()
fo.close()

outFileDiff = open(sys.argv[3], "w")

#for i in fileNew:
#        if not i in fileOld:
#                outFileDiff.write(i)
diff = difflib.context_diff(fileNew, fileOld, n=1)
outFileDiff.write(''.join(diff))

outFileDiff.close()
