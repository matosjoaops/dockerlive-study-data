import sys
import csv
import datetime

participant_id = sys.argv[1]

def rename_keys(data, task_num):
    data_copy = data.copy()
    for key in data_copy:
        new_key = f"{key} (Task {task_num})"
        data[new_key] = data.pop(key)

def parse_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, "%M:%S")

def delta_to_seconds(delta):
    return int(delta.total_seconds())

def setup_contexts(data):
    contexts = ["Reading Instructions", "Firefox", "Terminal", "VSCode", "File Manager", "File Editor", "Excluded"]
    for context in contexts:
        if context not in data:
            data[context] = 0

def process_task(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        data = {}
        first_timestamp = None
        most_recent_timestamp = None
        most_recent_context = None
        last_timestamp = None
        data["Context Switches"] = 0
        data["Total Duration"] = 0

        setup_contexts(data)

        for row in reader:
            if first_timestamp is None:
                first_timestamp = parse_timestamp(row["Timestamp"])

            if row["Context"] == "End":
                last_timestamp = parse_timestamp(row["Timestamp"])
                total_time = last_timestamp - first_timestamp
                data["Total Duration"] += delta_to_seconds(total_time)

            if most_recent_timestamp is not None and most_recent_context is not None:
                time_since_last_context_change = parse_timestamp(row["Timestamp"]) - most_recent_timestamp
                time_in_seconds = delta_to_seconds(time_since_last_context_change)
                data[most_recent_context] += time_in_seconds
                if most_recent_context == "Excluded":
                    data["Total Duration"] -= time_in_seconds
                    data["Context Switches"] -= 1
 
            most_recent_context = row["Context"]
            most_recent_timestamp = parse_timestamp(row["Timestamp"])
            data["Context Switches"] += 1
        
        data["Context Switches"] -= 1 #"End" doesn't count

        return data

task_1_data = process_task(f"anon-data/individual-tasks/{participant_id}/task-1.csv")
task_2_data = process_task(f"anon-data/individual-tasks/{participant_id}/task-2.csv")
task_3_data = process_task(f"anon-data/individual-tasks/{participant_id}/task-3.csv")

with open(f"anon-data/participants.csv", "a") as file:
    rename_keys(task_1_data, 1)
    rename_keys(task_2_data, 2)
    rename_keys(task_3_data, 3)
    merged_data = {}
    merged_data["id"] = participant_id
    merged_data |= task_1_data | task_2_data | task_3_data

    values = list(map(lambda x: str(x),merged_data.values()))

    file.write(",".join(values) + "\n")

