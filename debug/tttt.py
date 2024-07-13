file_path = "H:\\app-uiauto-test-dev\\debug\\test.txt"

with open(file_path, 'r') as file:
    for line in file:
        print(line.strip())