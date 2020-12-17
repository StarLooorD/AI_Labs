import numpy as np

r, c = input().split()

lab = []

for i in range(int(r)):
    lab.append(input())

start = 0, 0
end = [int(r) - 1, int(c) - 1]
mirrored = np.zeros((int(r), int(c)))
i, j = start
mirrored[i][j] = 1


def make_step(k):
    for i in range(len(mirrored)):
        for j in range(len(mirrored[i])):
            if mirrored[i][j] == k:
                if i > 0 and mirrored[i - 1][j] == 0 and lab[i - 1][j] == '.':
                    mirrored[i - 1][j] = k + 1
                if j > 0 and mirrored[i][j - 1] == 0 and lab[i][j - 1] == '.':
                    mirrored[i][j - 1] = k + 1
                if i < len(mirrored) - 1 and mirrored[i + 1][j] == 0 and lab[i + 1][j] == '.':
                    mirrored[i + 1][j] = k + 1
                if j < len(mirrored[i]) - 1 and mirrored[i][j + 1] == 0 and lab[i][j + 1] == '.':
                    mirrored[i][j + 1] = k + 1


k = 0
i, j = end
zero = False
while mirrored[end[0]][end[1]] == 0:
    k += 1
    make_step(k)
    if k > i*j:
        zero = True
        break



print(mirrored)

if zero:
    print('ZERO')
else:
    i, j = end
    k = mirrored[i][j]
    many = False
    while k > 1:
        counter = 0
        if i > 0 and mirrored[i - 1][j] != 0:
            counter += 1
        if j > 0 and mirrored[i][j - 1] != 0:
            counter += 1
        if i < len(mirrored) - 1 and mirrored[i + 1][j] != 0:
            counter += 1
        if j < len(mirrored[i]) - 1 and mirrored[i][j + 1] != 0:
            counter += 1
        k -= 1
        if counter > 1:
            many = True
            print('MANY')
            break
    if not many:
        print('ONE')


