with open("map2.txt") as file:
    lines = [line.strip() for line in file]

pos = []
print(lines)
a = lines[0]
pos = [a[1:-1].split(", ") for a in lines]
# x, y  = a[1:-1].split(", ")
# x, y = int(x), int(y)
print(pos)
for p in pos:
    print(int(p[0]), int(p[1]))