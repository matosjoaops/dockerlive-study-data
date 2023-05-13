import csv

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

def anonymize_background(num_assignment):
    with open("data/background.csv", "r") as file:
        reader = csv.DictReader(file)
        with open("anon-data/background.csv", "w") as new_file:
            writer = csv.writer(new_file)
            wrote_header = False
            for row in reader:
                row.pop("Carimbo de data/hora")
                row.pop("Are you willing and interested to participate in this study?")
                row.pop("What is your name?")
                email = row["What is your email address?"]
                row.pop("What is your email address?")
                row["id"] = num_assignment[email]
                # print()
                # print(row)
                if not wrote_header:
                    writer.writerow(row)
                    wrote_header = True
                writer.writerow(row.values())


num_assignment = {}
        
with open("data/participant_num.csv", "r") as assignment_file:
    reader = csv.DictReader(assignment_file, fieldnames=["email", "num"])
    for row in reader:
        num_assignment[row["email"]] = row["num"]

anonymize_group("control.txt", num_assignment)
anonymize_group("experimental.txt", num_assignment)
anonymize_background(num_assignment)
