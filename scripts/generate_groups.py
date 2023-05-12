import random

file = open("data/participants.txt", "r")

file_content = file.read()

participants = file_content.splitlines()

num_participants = len(participants)

is_odd = (num_participants % 2 != 0)

num_people_per_group = num_participants // 2

list1 = [True] * num_people_per_group
list2 = [False] * num_people_per_group

if is_odd:
    rand_bool = bool(random.getrandbits(1))
    if rand_bool:
        list1.append(True)
    else:
        list2.append(False)

final_list = list1 + list2

random.shuffle(final_list)

exp_group = []
ctrl_group = []

for i in range(len(final_list)):
    if final_list[i]:
        exp_group.append(participants[i])
    else:
        ctrl_group.append(participants[i])


print("Experimental group:")
print(exp_group)

print("Control group:")
print(ctrl_group)