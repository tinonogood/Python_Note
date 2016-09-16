#!/usr/bin/env python

# def f(x):
#     return 5 * x * x + x + 5 # 需宣告回傳"return"
    # 5 * x * x + x + 5
# print(f(1))
#
# def g(x):
#     return 5 * x * x + f(x) + 5
# print(g(1))

# def g(x, y):  #需定義所需自變數
#     return 5 * y * y + f(x) + 5
# print(g(1, 1))
#
# a = [1, 2, 3, 4]
# print(g(a, 2)) #無法將list塞入

# def say_hello(words = None): #使用none會將"None"當預設值而給出"none"字串, 直接給空字串當default
#     print('Hi ' + str(words))
#
# say_hello()


# def say_hello(words=''):
#     print('Hi ' + words)
#
#
# def say_hello(w1='', w2=''):
#     print('Hi ' + w1 + w2)

# def say_hello(*words): #使用迴圈,以應付多個item的情況
#     # sentence = ''
#     # for w in words:
#     #     sentence += w + ' '
#     # print('Hi ' + sentence)
#     print('Hi ' + ', '.join(words)) # 或者用join(),處理多個item
#
# say_hello("tino")
# say_hello("tino2", "tino1")
# say_hello("tino2", "tino1", 't3')

#
# def show_element(e, x=0, y=0, z=0): # 呈現元素及座標
#     print(e)
#     print(x)
#     print(y)
#     print(z)
# show_element("H", 1, 1) # 依序賦予變數值
# show_element("H", y=1, z=1) # 指定變數值

# def show_element2(e, *coordinate): #將第一個item給定變數代號"e"
#     print(e)
#     print(coordinate)
#
# show_element2("H", 1, 1, 1)
#
# def show_dict(dict): #dict用於method
#     for k, v in dict.items():
#         print(k, v)
#
# show_dict({'a':1, 'b':2})

a = 123 # global變數,依層(見下例)

def f1():
    print(a) #此層無變數a故向上索取,依此類推
# f1() # =123

def f2():
    a = 22
    print(a) #此層變數a修改
f2() # =22
f1() # =123

def f3(a):
    print(a) # =自己給定

def f4(l):
    l = 345
    print(l)

f4(a) # = 345
print(a) # = 123


def f5(l):
    l = [345]
    print(l)

b = [1,2,3]

f5(b) # = [345], b[1,2,3]帶入後,被l = [345]修改
print(b)


def f6(l):
    l.append(7)
    print(l)

c = [1,2,3]

f6(c) #append一個7,並改寫List c, 保存原本list可用deepcopy

print(c) #被改寫的list c
f6(c) #再append一個7
