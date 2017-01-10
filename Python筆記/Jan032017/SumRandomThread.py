# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 06:44:06 2017

@author: tino
"""

#!/usr/bin/python

import threading

random = 7

class myThread (threading.Thread):
    def __init__(self, threadID, name, x, ans, random):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.x = x
        self.ans = ans
        self.random = random
    def run(self):
        print("Starting " + self.name)
        threadLock.acquire()
#        print(tailrecSum(self.x, self.random))
        self.ans = tailrecSum(self.x, self.random)
        print(self.ans)
        threadLock.release()
        
def tailrecSum(x, random, sum=0):
    if x > 100:
        return sum
    else:
#        print(x)
        return tailrecSum(x + random, random, sum + x)
        
#print(tailrecSum(0, random))
        
threadLock = threading.Lock()
threads = []
answers = []    
    
def creatThread(random):
    for i in range(1,random+1):
        i = myThread(i, "Thread-" + str(i) , i, 0 , random)
        i.start()
#        print(i.ans)
        threads.append(i)
        answers.append(i.ans)
    
creatThread(random)

for t in threads:
    t.join()
    
print("Exiting Main Thread")

print(answers)

print(sum(answers))
    

    
