# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:59:17 2017

@author: tino
"""

import threading
import time

class AsyncWrite(threading.Thread):
    def __init__(self, text, out):
        threading.Thread.__init__(self)
        self.text = text
        self.out = out

    def run(self):
        f = open(self.out, "a")
        f.write(self.text + '\n')
        f.close()
        time.sleep(2)
        print("Finished Background file write to " + self.out)
        

def Main():
    message = input("Enter a string to store:" )
    background = AsyncWrite(message, 'out.txt')
    background.start()
    print("The program can continue while it writes in another thread")
    print("100 + 400 = ", 100+400)

    background.join()
    print("Waited until thread was complete")

if __name__ == '__main__':
    Main()