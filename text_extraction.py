path = 'result.txt'

with open(path) as f:
    lines = f.readlines()

count1 = 0
count2 = 0
count3 = 0
count4 = 0

for line in lines:
    if(line == "player1\n"):
        count1 += 1
    elif(line == "player2\n"):
        count2 += 1
    elif(line == "player3\n"):
        count3 += 1
    elif(line == "player4\n"):
        count4 += 1
    # print(line)

print(f"Player1：{count1}勝")
print(f"Player2：{count2}勝")
print(f"Player3：{count3}勝")
print(f"Player4：{count4}勝")

print(f"勝率：{count1/(count1+count2+count3+count4)}")
