import random
small_list = [0, 0, 0, 0, 0]
resource_list = []
# for i in range(1000000):
#     for j in range(5):
#         small_list.append(random.randint(0,4))
#     resource_list.append(small_list)
#     small_list=[]

count = 0
for i in range(20):
    for make in range(100000):
        for j in range(i):
            num = random.randint(0, 4)
            small_list[num] += 1
        resource_list.append(small_list)
        small_list = [0, 0, 0, 0, 0]

# resource_list = [tuple(i) for i in resource_list]
# resource_list = list(set(resource_list))
# resource_list = [list(i)for i in resource_list]
# resource_list = [[2, 0, 2, 13, 3]]

# print(resource_list)
#

# 0: ore,1: brick, 2: wheat, 3: wood, 4: sheep
# resourceList=[ORE,BRICK,WHEAT,WOOD,SHEEP]
resource_dict = {}
list1 = []  # 全部×
list2 = []  # cityのみ
list3 = []  # roadのみ
list4 = []  # c&s→全部○では
list5 = []  # c&r
list6 = []  # s&r
list7 = []  # 全部○

for i in resource_list:
    if((i[3] == 0 or i[1] == 0) and (i[0] <= 2 or i[2] <= 1)):
        list1.append(i)
    elif((i[0] >= 3 and i[2] >= 2) and (i[1] == 0 or i[3] == 0)):
        list2.append(i)
    elif((i[1] >= 1 and i[3] >= 1) and (i[2] == 0 or i[4] == 0) and (i[0] <= 2 or i[2] <= 1)):
        list3.append(i)
    elif((i[0] >= 3 and i[2] >= 2) and (i[1] >= 1 and i[2] >= 1 and i[3] >= 1 and i[4] >= 1)):
        list4.append(i)
    elif((i[0] >= 3 and i[2] >= 2) and (i[1] >= 1 and i[3] >= 1)):
        list5.append(i)
    elif(i[1] >= 1 and i[2] >= 1 and i[3] >= 1 and i[4] >= 1):
        list6.append(i)
    else:
        list7.append(i)

resource_dict[0] = list1
resource_dict[1] = list2
resource_dict[2] = list3
resource_dict[3] = list4
resource_dict[4] = list5
resource_dict[5] = list6

# print(resource_dict)

# print(list3)

# print(resource_dict[0])
# if(len(resource_list) == len(list1)+len(list2)+len(list3)+len(list4)+len(list5)+len(list6)):
#     print("ok")
# else:
#     print(len(list1)+len(list2)+len(list3)+len(list4)+len(list5)+len(list6))
#     print(list7)

# data_set = set(resource_list)
# print(data_set)

# resource_dict={1:,2:,3:,4:,5:,6:,7:}
