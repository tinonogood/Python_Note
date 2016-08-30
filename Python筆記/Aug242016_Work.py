import re

data = """B10231011:x:1067:1000:Su Lin-Ya,,0910-622-175:/home/B10231011:/bin/bash
B10206009:x:1068:1000:JI-BING-CHEN,,0910246189:/home/B10206009:/bin/bash
B10206035:x:1070:1000:ZHANG-JIE-KAI,,0970663675:/home/B10206035:/bin/bash
B10206031:x:1071:1000:LI ZHE-CHENG,,0903008989:/home/B10206031:/bin/bash
D10406811:x:1072:1000:jemal yimer damte,,0965668144:/home/D10406811:/bin/bash
M10406013:x:1073:1000:wang kai-ting,,0988148729:/home/M10406013:/bin/bash
B10206022:x:1074:1000:SU-BO-CHENG,,0970623878:/home/B10206022:/bin/bash
M10406009:x:1075:1000:Yu Ching,,0987930004:/home/M10406009:/bin/bash
tino:x:1076:1000:Kaiting wang,,0988148729:/home/tino:/bin/bash
ychungn:x:1077:1000:Hung Ying Chieh,,0975207247:/home/ychungn:/bin/bash
D10306103:x:1078:1000:Yu-Cheng Liu,,0960537760:/home/D10306103:/bin/bash
D10406817:x:1079:1000:Dhana Lakshmi Busipalli,0966747020:/home/D10406817:/bin/bash
chya:x:1080:1000:chya,0956015982:/home/chya:/bin/bash
"""

#使用者輸入
search_member = "D10406817"
default_value = "User not exist"

member_info = re.split(":|\n", data) #資料處裡 by re_module, 依":"和"\n"分割

#迴圈練習
for member in member_info:
    if search_member == member:
        i = member_info.index(search_member)
        print("Account: " + member_info[i] + "\n" +
              "UID: " + member_info[i+2] + "\n" +
              "GID: " + member_info[i+3] + "\n" +
              "Name, phone#: " + member_info[i+4] + "\n"
              )

#setdefault練習

member_info2 = re.split(":x:|\n", data) #資料處裡 by re_module, 依":x:"和"\n"分割

#轉換list to hashmap
member_info2_length = len(member_info2)
#print(member_info2_length)

member_account = ["User"]
member_information = ["Info"]
for a in range(member_info2_length-3, -2, -2): #使用loop與 range(起始, 結束, 步距)
    member_account.append(member_info2[a]) #append()將資料附上
for b in range(member_info2_length-2, 0, -2):
    member_information.append(member_info2[b])

result = dict(zip(member_account, member_information))
result.setdefault(search_member, default_value)
print("User Info: " + result[search_member])
