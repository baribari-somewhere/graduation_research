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

print(np.random.permutation(
    [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]))

port_pair_list = [[43, 44], [33, 34], [45, 49], [27, 53], [
    24, 29], [30, 31], [36, 39], [41, 42], [51, 52]]
randomPortIndices = np.random.permutation(
    [i for i in range(len(port_pair_list))])

print(randomPortIndices)
