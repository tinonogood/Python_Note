print("Hello Python!") # method print()

PI = 3.14 # 常數大寫
DAY_OF_YEAR = 365
first_name = 'Bary' # python習慣用單引號, 但都無差
last_name = "Fu"
print(PI)

print(DAY_OF_YEAR / 3) # python無型態限制(int, float, double)

print(first_name, last_name) # print 多變數,以","分開

print(first_name == "Bary") #條件判斷

print("day" in "Friday") #str包含判斷

print(len(first_name)) # method len():得字串長度

print(first_name[::2]) # 字串切片(slice) [起始:結束:步距]

# example
#   +---+---+---+---+---+ 
#   | H | e | l | p | A |
#   +---+---+---+---+---+ 
#   0   1   2   3   4   5 
#  -5  -4  -3  -2  -1





weeks = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] #list以"[]"儲存item
for day in weeks: # for迴圈 將list中item依次跑過
    if day == "Saturday" or day == "Sunday":
        print("Holiday is : " + day)
    else:
        print("Workday is : " + day )

input_day = "FRI" #變數小寫

for day in weeks:
    if input_day.lower() in day.lower(): #method: lower()置換小寫;upper()置換大寫
        print(day)
    else:
        print(None)



week = {'mon': "Monday",
        'tues': "Tuesday",
        'wed': "Wednesday",
        'thur': "Thursday",
        'fri': "Friday",
        'sat': "Saturday",
        'sun': "Sunday"} #"{}"儲存hash,dic(key:value)

week.setdefault(input_day.lower(), 'None') #用法: dict.setdefault(key, default),若key 在dict中，回傳value 值，反之，將 key:default 加入 dict 之中
print(week[input_day.lower()]) #將key: input_day.lower()塞入week並回傳其value


pork = {'A': 1, 'K': 13, 'Q':12}
# print(pork['J'] )

pork_number = 'A'
default_val=0 #default_val提出處理

pork.setdefault(pork_number, default_val)
# if not(pork_number in pork.keys()):
#     pork[pork_number] = default_val

print(pork[pork_number])
