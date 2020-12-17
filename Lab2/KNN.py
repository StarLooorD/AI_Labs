n, k, m = [int(i) for i in input().split()]
wi = []
hi = []
wj = []
hj = []
for i in range(n):
    a, b = [int(i) for i in input().split()]
    wi.append(a)
    hi.append(b)
for i in range(m):
    a, b = [int(i) for i in input().split()]
    wj.append(a)
    hj.append(b)
d = {}
for j in range(m):
    d[j] = []
    for i in range(n):
        d[j].append(max(abs(wi[i] - wj[j]), abs(hi[i] - hj[j])))
answer = []
if k > n:
    k = n
for i in range(len(d)):
    temp = []
    for j in range(k):
        temp.append(d[i].index(min(d[i])) + 1)
    counters = []
    print(temp)
    for item in temp:
        counters.append(temp.count(item))
    counters.sort()
    answer.append(temp[counters.index(max(counters))])
print(' '.join(str(i) for i in answer))