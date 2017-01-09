# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 02:04:46 2017

@author: tino
"""

#!/usr/bin/python

import threading

class myThread (threading.Thread):
    def __init__(self, threadID, name, x, ans):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.x = x
        self.ans = ans
    def run(self):
        print("Starting " + self.name)
        threadLock.acquire()
        print(tailrecSum(self.x))
        self.ans = tailrecSum(self.x)
        threadLock.release()
        
def tailrecSum(x, sum=0): #尾遞迴,減少記憶體調用
    if x > 100:
        return sum
    else:
        return tailrecSum(x+4, sum + x)
        
threadLock = threading.Lock()
threads = []
    
thread1 = myThread(1, "Thread-1", 1, 0)
thread2 = myThread(2, "Thread-2", 2, 0)
thread3 = myThread(3, "Thread-3", 3, 0)
thread4 = myThread(4, "Thread-4", 4, 0)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)

for t in threads:
    t.join()
    
print(thread1.ans + thread2.ans + thread3.ans + thread4.ans)

print("Exiting Main Thread")