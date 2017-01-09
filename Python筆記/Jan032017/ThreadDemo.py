# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 19:51:28 2017

@author: tino
"""

#!/usr/bin/python

import _thread
import time

# Define a function for the thread
def print_time(threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print ("Error: unable to start thread")

#while 1:    #無法中斷程式
#   pass

while 0:    #離開程式,thread繼續
    pass
