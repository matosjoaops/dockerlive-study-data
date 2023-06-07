import sys
import csv

def add_times(time1, time2):
    nums1 = time1.split(":")
    nums2 = time2.split(":")

    m1 = int(nums1[0])
    s1 = int(nums1[1])

    m2 = int(nums2[0])
    s2 = int(nums2[1])

    m = m1 + m2
    if s1 + s2 >= 60:
        m += 1
    s = (s1 + s2) % 60
    str_m = str(m)
    str_s = str(s)

    if s < 10:
        str_s = "0" + str_s

    if m < 10:
        str_m = "0" + str_m

    return f"{str_m}:{str_s}"

if len(sys.argv) < 2:
    print("Need arg!")
    exit(1)

filename = sys.argv[1]
new_timestamps = []

with open(filename, "r") as file:
    reader = csv.DictReader(file)

    previous_video_timestamp = None
    first_after_fail = False
    time_to_subtract = None

    for row in reader:
        context = row["Context"]
        timestamp = row["Timestamp"]

        if first_after_fail:
            first_after_fail = False
            time_to_subtract = "00:" + str(-int(timestamp.split(":")[1]))

        if previous_video_timestamp != None:
            new_timestamp = add_times(add_times(previous_video_timestamp, time_to_subtract), timestamp)
            timestamp = new_timestamp

        if "fail" in context:
            previous_video_timestamp = timestamp
            first_after_fail = True
        else:
            new_timestamps.append((context, timestamp))

with open(filename, "w") as file:
    file.write("Context,Timestamp\n")
    for i in new_timestamps:
        file.write(i[0] + "," + i[1] + "\n")