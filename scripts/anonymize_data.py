import csv
import os
import shutil

def anonymize_group(filename, num_assignment):
    with open(f"data/{filename}", "r") as file:
        content = file.read()
        lines = content.splitlines()
        if lines[-1] == "":
            lines.pop()
        new_file_content = ""
        for line in lines:
            new_file_content += num_assignment[line] + "\n"
        with open(f"anon-data/{filename}", "w") as new_file:
            new_file.write(new_file_content)

def anonymize_questionnaire(filename, num_assignment):
    with open(f"data/{filename}", "r") as file:
        reader = csv.DictReader(file)
        with open(f"anon-data/{filename}", "w") as new_file:
            writer = csv.writer(new_file)
            wrote_header = False
            for row in reader:
                row.pop("Carimbo de data/hora")
                if "Are you willing and interested to participate in this study?" in row:
                    row.pop("Are you willing and interested to participate in this study?")
                row.pop("What is your name?")
                email = row["What is your email address?"]
                row.pop("What is your email address?")
                row["id"] = num_assignment[email]

                if not wrote_header:
                    writer.writerow(row)
                    wrote_header = True
                writer.writerow(row.values())

def anonymize_dockerfiles(num_assignment):
    for email, id in num_assignment.items():
        old_path = f"data/Dockerfiles/{email}"
        if os.path.exists(old_path):
            new_path = f"anon-data/Dockerfiles/{id}"
            os.makedirs(new_path, exist_ok=True)

            tasks = [1, 2, 3]
            for task in tasks:
                old_filename = f"{old_path}/Dockerfile.{email}.task-{task}"
                new_filename = f"{new_path}/Dockerfile.task-{task}"
                shutil.copy(old_filename, new_filename)
        else:
            continue

num_assignment = {}
        
with open("data/participant_id.csv", "r") as assignment_file:
    reader = csv.DictReader(assignment_file, fieldnames=["email", "num"])
    for row in reader:
        num_assignment[row["email"]] = row["num"]

anonymize_group("control.txt", num_assignment)
anonymize_group("experimental.txt", num_assignment)
anonymize_questionnaire("background.csv", num_assignment)
anonymize_questionnaire("control_questionnaire.csv", num_assignment)
anonymize_questionnaire("experimental_questionnaire.csv", num_assignment)
anonymize_dockerfiles(num_assignment)
