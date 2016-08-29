#!/usr/bin/env/python

import sys
from datetime import datetime
import numpy as np

# 展示python, numpy向量加法中運行時間差異
# 
# python vectorsum.py n
#
# n 可為任意整數,得其次方和,立方和與計算時間

def numpysum(n):
    a = np.arange(n) ** 2 # 創n個元素的numpy數組並次方
    b = np.arange(n) ** 3 # 立方
    c = a + b

    return c


def pythonsum(n):
    a = range(n)
    b = range(n)
    c = []

    for i in range(len(a)):
        a[i] = i ** 2
        b[i] = i ** 3
        c.append(a[i] + b[i])

    return c

size = int(sys.argv[1]) # 讀取第一個使用者輸入並使其為size變數

start = datetime.now() # 讀取系統時間為start,起始時間
c = pythonsum(size)
delta = datetime.now() - start # 系統時間 - 起始時間 為delta時間差
print "Last 2 elements: ", c[-2:] # slice 讀出(倒數第二起始)後兩者
print "PythonSum in ms: ", delta.microseconds
start = datetime.now()
c = numpysum(size)
delta = datetime.now() - start
print "Last 2 elements: ", c[-2:]
print "NumPySum in ms: ", delta.microseconds
