# print("Hello Python!")
#
# PI = 3.14
# DAY_OF_YEAR = 365
first_name = 'Bary'
last_name = "Fu"
#
# print(PI)
# print(DAY_OF_YEAR / 3)
# print(first_name, last_name)
#
# print(first_name == "Bary")
#
# print("day" in "Friday")
#
# print(len(first_name))

print(first_name[::2])





weeks = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for day in weeks:
    if day == "Saturday" or day == "Sunday":
        print("Holiday is : " + day)
    else:
        print("Workday is : " + day )

input_day = "FRI"

for day in weeks:
    if input_day.lower() in day.lower():
        print(day)
    else:
        print(None)



week = {'mon': "Monday",
        'tues': "Tuesday",
        'wed': "Wednesday",
        'thur': "Thursday",
        'fri': "Friday",
        'sat': "Saturday",
        'sun': "Sunday"}

week.setdefault(input_day.lower(), 'None')
print(week[input_day.lower()])






pork = {'A': 1, 'K': 13, 'Q':12}
# print(pork['J'] )

pork_number = 'A'
default_val=0

pork.setdefault(pork_number, default_val)
# if not(pork_number in pork.keys()):
#     pork[pork_number] = default_val

print(pork[pork_number])