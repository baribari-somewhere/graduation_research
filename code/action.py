

action = [
    ["dp"],
    ["up"],
    ["p"],
    [(0, 1), "Rp"],
    [(0, 5), "Rp"],
    [(0, 12), "Rp"],
    [(1, 2), "Rp"],
    [(1, 6), "Rp"],
    [(2, 3), "Rp"],
    [(2, 9), "Rp"],
    [(3, 4), "Rp"],
    [(3, 19), "Rp"],
    [(4, 5), "Rp"],
    [(4, 16), "Rp"],
    [(5, 14), "Rp"],
    [(6, 7), "Rp"],
    [(6, 11), "Rp"],

    [(7, 8), "Rp"],
    [(7, 24), "Rp"],
    [(8, 9), "Rp"],
    [(8, 27), "Rp"],
    [(9, 22), "Rp"],
    [(10, 11), "Rp"],
    [(10, 12), "Rp"],
    [(10, 32), "Rp"],
    [(11, 28), "Rp"],
    [(12, 13), "Rp"],
    [(13, 15), "Rp"],
    [(13, 34), "Rp"],
    [(14, 15), "Rp"],

    [(14, 18), "Rp"],
    [(15, 36), "Rp"],
    [(16, 17), "Rp"],
    [(16, 21), "Rp"],
    [(17, 18), "Rp"],
    [(17, 40), "Rp"],
    [(18, 38), "Rp"],
    [(19, 20), "Rp"],
    [(19, 23), "Rp"],
    [(20, 21), "Rp"],
    [(20, 45), "Rp"],
    [(21, 43), "Rp"],

    [(22, 23), "Rp"],
    [(22, 50), "Rp"],
    [(23, 48), "Rp"],
    [(24, 25), "Rp"],
    [(24, 29), "Rp"],
    [(25, 26), "Rp"],
    [(26, 27), "Rp"],
    [(27, 53), "Rp"],
    [(28, 29), "Rp"],
    [(28, 31), "Rp"],
    [(30, 31), "Rp"],
    [(30, 32), "Rp"],

    [(32, 33), "Rp"],
    [(33, 34), "Rp"],
    [(34, 35), "Rp"],
    [(35, 37), "Rp"],
    [(36, 37), "Rp"],
    [(36, 39), "Rp"],
    [(38, 39), "Rp"],
    [(38, 42), "Rp"],
    [(40, 41), "Rp"],
    [(40, 44), "Rp"],
    [(41, 42), "Rp"],
    [(43, 44), "Rp"],

    [(43, 47), "Rp"],
    [(45, 46), "Rp"],
    [(45, 49), "Rp"],
    [(46, 47), "Rp"],
    [(48, 49), "Rp"],
    [(48, 52), "Rp"],
    [(50, 51), "Rp"],
    [(50, 53), "Rp"],
    [(51, 52), "Rp"]
]

for i in range(54):
    action.append([str(i), "Sp"])
    action.append([str(i), "Cp"])


def sample(obj):

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


ACTION = action

# sample(action[3][0])
# print(action[3][0])
# for i in action:
#     sample(action[0])
print(len([(1, 2), 2]))
# print(action)
# l = (1, 3, 2, 3, 1)
