def factorial(n): #迴圈連加
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum    
    
print(factorial(5)) 


def summary(n): ＃遞迴連加
    if 0 == n:
        return 0
    else:
        return n + summary(n-1)
    
print(summary(5))


def tailrecSum(x, sum=0): #尾遞迴,減少記憶體調用
    if x == 0:
        return 0
    else:
        return tailrecSum(x-1, sum + x)
  


class First(object):
    def say(self):
        print("from First")

class Second(object):
    def say(self):
        print("from Second")

class Third(object):
    def say(self):
        print("from Third")

class Son(First, Second, Third): ＃繼承First,Second,Third super()指的是 MRO 中的下一個，而不是父類
    def say(self): 
        #super().say() # from First (same as super(Son, self).say())
#        super(First, self).say() # from Second
        super(Second, self).say() # from Third 
        #super(Third, self).say() # error

son = Son()
son.say()
        
