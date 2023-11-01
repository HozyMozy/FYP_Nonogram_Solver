R = 6
C = 5
grid = [[0 for x in range(C)] for y in range(R)]
for x in grid:
    print(x)

l1 = [2,0]
l2 = [2, 1]
l1 = [i for i in l1 if i != 0]
print(l1 < l2)
