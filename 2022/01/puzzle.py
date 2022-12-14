with open("input.txt", "r") as file:
    lines = [line.strip() for line in file.readlines()]

group = 0
groups = []

for line in lines:
    if line == "":
        groups.append(group)
        group = 0
    else:
        group += int(line)
groups.append(group)

groups.sort()
print(groups[-1])
print(groups[-2])
print(groups[-3])

total = groups[-1]+groups[-2]+groups[-3]
print(total)
print(sum(groups[-1:-4:-1]))