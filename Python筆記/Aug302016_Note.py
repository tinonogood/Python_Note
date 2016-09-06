#!/usr/bin/env python

# array,list:中括; haspmap,set:大括; tuple: 小括

import copy
a = [10, 9, 8, 7]
b = [1, 2, 3, 1, 2, 4]

print(b)
print(b[0] ** 2)

for var in b:
    print(var ** 2)


s = set(b) #將list轉成set
print(s)

print(a)

a.append("JJC") #List附加上新element
a.append([1, 2, 3, 5]) #List附加上新list, 第二層

print(a + b) #list合併


c = copy.deepcopy(a) #reverse將List值反轉,若需要得反轉的list且保留原本值,可將a的reference deepcopy至新記憶體位置以供利用
c.reverse()
# c = reversed(a) #提供記憶體位置，而非儲存值


# # print(a[::-1]) #反轉=步距:-1
# print(a)
# print(c)
#
# a.sort()
print(sorted(a))
print(a)


dict = {'a' : 3, 'b' : 2, 'c' : 1}

print(dict) #dict, hashmap並無排序性

print(dict['a'])
#
for var in dict.keys(): #將dict的key, loop給入變數var
    print(var)
    print(dict[var])

for k, v in dict.items(): #將dict的 "key與value" 給入變數k與v
    print(k, v)
#
#
import enum

class Shake(enum.Enum): #避免瑣碎的定義, value不可重複(相對於hashmap: key不能重複)
    vanilla = 7
    chocolate = 4
    cookies = 9
    mint = 7

for shake in Shake:
    print(shake)



x = [1, 2, 3]  # "==" vs "is"

if x == [1, 2, 3]: # ==: value相同
    print('OK1')

if x is [1, 2, 3]: # is: 記憶體指向obj位置相同, 此處不成立
    print('OK2')

#  "strin"+"g" is "string"
#  True
#  s1 = "strin"
#  s2 = "string"
#  s1+"g" is s2
#  False
