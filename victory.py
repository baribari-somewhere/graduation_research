path = './teacher8_victory_10300.txt'

with open(path) as f:
    lines = f.readlines()

count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0
count11 = 0


for line in lines:
    # print(line)
    if(line == "2\n"):
        count2 += 1
    elif(line == "3\n"):
        count3 += 1
    elif(line == "4\n"):
        count4 += 1
    elif(line == "5\n"):
        count5 += 1
    elif(line == "6\n"):
        count6 += 1
    elif(line == "7\n"):
        count7 += 1
    elif(line == "8\n"):
        count8 += 1
    elif(line == "9\n"):
        count9 += 1
    elif(line == "10\n"):
        count10 += 1
    elif(line == "11\n"):
        count11 += 1
    # print(line)

# print(f"Player1：{count1}勝")
# print(f"Player2：{count2}勝")
# print(f"Player3：{count3}勝")
# print(f"Player4：{count4}勝")

# print(f"勝率：{count1/(count1+count2+count3+count4)}")
print([count2, count3, count4, count5, count6,
      count7, count8, count9, count10, count11])
