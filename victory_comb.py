path = './comb_victory_NoFRG_500.txt'

with open(path, encoding="utf-8") as f:
    lines = f.readlines()

count1_A = 0
count2_A = 0
count3_A = 0
count4_A = 0
count5_A = 0
count6_A = 0
count7_A = 0
count8_A = 0
count9_A = 0
count10_A = 0
count11_A = 0

count1_B = 0
count2_B = 0
count3_B = 0
count4_B = 0
count5_B = 0
count6_B = 0
count7_B = 0
count8_B = 0
count9_B = 0
count10_B = 0
count11_B = 0

max_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

turn_count = []
flag = False
flag2 = False
skip = False
turn_all = 0
turn_lose = 0
turn_win = 0
count_win = 0
count_lose = 0
for line in lines:
    # print(line)
    # skip = False
    # flag=False
    if(skip == False):
        # print(line[18])
        skip = True
        save = int(line[8])
        if(line[8] == "2"):
            count2_A += 1
        elif(line[8] == "3"):
            count3_A += 1
        elif(line[8] == "4"):
            count4_A += 1
        elif(line[8] == "5"):
            count5_A += 1
        elif(line[8] == "6"):
            count6_A += 1
        elif(line[8] == "7"):
            count7_A += 1
        elif(line[8] == "8"):
            count8_A += 1
        elif(line[8] == "9"):
            count9_A += 1
        elif(line[8] == "1" and line[9] == "0"):
            count10_A += 1
            flag = True
            save = 10
        elif(line[8] == "1" and line[9] == "1"):
            count11_A += 1
            flag = True
            save = 10
        if(line[9] == ","):
            if(line[18] == "2"):
                count2_B += 1
            elif(line[18] == "3"):
                count3_B += 1
            elif(line[18] == "4"):
                count4_B += 1
            elif(line[18] == "5"):
                count5_B += 1
            elif(line[18] == "6"):
                count6_B += 1
            elif(line[18] == "7"):
                count7_B += 1
            elif(line[18] == "8"):
                count8_B += 1
            elif(line[18] == "9"):
                count9_B += 1
            elif(line[18] == "1" and line[19] == "0"):
                count10_B += 1
                flag = True
                save = 10
            elif(line[18] == "1" and line[19] == "1"):
                count11_B += 1
                flag = True
                save = 10
            if(save < int(line[18])):
                save = int(line[18])
        else:
            if(line[19] == "2"):
                count2_B += 1
            elif(line[19] == "3"):
                count3_B += 1
            elif(line[19] == "4"):
                count4_B += 1
            elif(line[19] == "5"):
                count5_B += 1
            elif(line[19] == "6"):
                count6_B += 1
            elif(line[19] == "7"):
                count7_B += 1
            elif(line[19] == "8"):
                count8_B += 1
            elif(line[19] == "9"):
                count9_B += 1
            elif(line[19] == "1" and line[20] == "0"):
                count10_B += 1
                flag = True
                save = 10
            elif(line[19] == "1" and line[20] == "1"):
                count11_B += 1
                flag = True
                save = 10
        max_list[save-2] += 1
    else:
        skip = False
        turn_all += int(line)
        if(flag):
            turn_count.append(int(line))
            flag = False
            turn_win += int(line)
            count_win += 1
        else:
            turn_lose += int(line)
            count_lose += 1

    # print(line)

# print(f"Player1：{count1}勝")
# print(f"Player2：{count2}勝")
# print(f"Player3：{count3}勝")
# print(f"Player4：{count4}勝")

# print(f"勝率：{count1/(count1+count2+count3+count4)}")
# print([count2, count3, count4, count5, count6,
#       count7, count8, count9, count10, count11])

print(f"playerA：{[count2_A, count3_A, count4_A, count5_A, count6_A,count7_A, count8_A, count9_A, count10_A, count11_A]}")
print(f"playerC：{[count2_B, count3_B, count4_B, count5_B, count6_B,count7_B, count8_B, count9_B, count10_B, count11_B]}")
print(f"max_list：{max_list}")
print(f"turn_count：{turn_count}")
print(f"total_av：{turn_all/10000}")
print(f"total_win：{turn_win/count_win}")
print(f"total_lose：{turn_all/count_lose}")
