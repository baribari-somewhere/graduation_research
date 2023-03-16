import numpy as np
list1 = []
list1.append((1, 2, 3))

dic = {(1, 2, 3): [1234]}


for i in dic.keys():
    if(list1[0] == i):
        print("ok")
    else:
        print("no")


def sample(obj):
    """ 引数の型を判定する """

    if isinstance(obj, bool):
        print('bool型です')

    if isinstance(obj, int):
        print('int型です')

    if isinstance(obj, float):
        print('float型です')

    if isinstance(obj, complex):
        print('complex型です')

    if isinstance(obj, list):
        print('list型です')

    if isinstance(obj, tuple):
        print('tuple型です')

    if isinstance(obj, range):
        print('range型です')

    if isinstance(obj, str):
        print('str型です')

    if isinstance(obj, set):
        print('set型です')

    if isinstance(obj, frozenset):
        print('frozenset型です')

    if isinstance(obj, dict):
        print('dict型です')


sample(list1[0])

a = (1, 2)
print(a[0])

# print(np.random.permutation(
#     [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]))

port_pair_list = [[43, 44], [33, 34], [45, 49], [27, 53], [
    24, 29], [30, 31], [36, 39], [41, 42], [51, 52]]
randomPortIndices = np.random.permutation(
    [i for i in range(len(port_pair_list))])

# print(randomPortIndices)
# print(len("Rp"))

def get_stage():
        stage = []
        a = ""
        f = open('stage_info.txt', 'r', encoding='UTF-8-sig')
        data = f.read().split("\n")
        skip = False
        for i in data:
            list_all = []
            list1 = []
            list2 = []
            count = 1
            # print(i)
            for j in i:
                # print(j)
                if(j.isdecimal() == True and skip == False):
                    # print(1)
                    a += j
                elif(skip == True):
                    skip = False
                # elif(j == ','):
                    # print(3)
                elif(j == "," and count == 1):
                    list_all.append([int(a)])
                    # print(2)
                    a = ""
                    count += 1
                elif(j == "."):
                    skip = True
                elif(j == "," and 1 < count and count <= 72):
                    list1.append(int(a))
                    a = ""
                    count += 1
                elif(j == "," and count == 73):
                    list1.append(int(a))
                    list_all.append(list1)
                    a = ""
                    count += 1
                elif(j == "," and 73 < count and count <= 126):
                    list2.append(int(a))
                    a = ""
                    count += 1
                elif(count == 127):
                    # print(111111111111111111111111111111111111111111111)
                    # list2.append(int(a))
                    list_all.append(list2)
                    a = ""
                    count += 1
            # print(list2)
            stage.append(list_all)
        return stage
    
stage=get_stage()
print(stage[1])
print(stage[1][1])
print(stage[1][2])