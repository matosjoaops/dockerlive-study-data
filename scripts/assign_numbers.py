import random

file = open("data/participants.txt", "r")

file_content = file.read()

participants = file_content.splitlines()

num_participants = len(participants)

num_list = list(range(num_participants + 1))

num_list.pop(0)

random.shuffle(num_list)

new_file_content = ""

for i in range(len(num_list)):
    new_file_content += participants[i] + "," + str(num_list[i]) + "\n"

new_file = open("data/participant_num.csv", "w")

new_file.write(new_file_content)