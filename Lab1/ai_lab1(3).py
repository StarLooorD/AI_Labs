import sys
sys.setrecursionlimit(1000000)


# DFS algorythm
def dfs_algo(v):
    global get_in_time
    global hours
    global visited_status

    # Math current node as visited and counting time to that node
    get_in_time[v] = hours
    hours += 1
    visited_status[v] = 'grey'

    # Checking if node has child so that we can take down and continue algorythm
    for i in range(len(connections[v])):
        next_v = connections[v][i]
        # We continue going if next node was not visited yet (has 'white' status)
        if visited_status[next_v] == 'white':
            dfs_algo(next_v)

    # If that node is last child we match it in 'black' color and obviously adding 1 hour to general time
    visited_status[v] = 'black'
    hours += 1


# Defining number of nodes, connections between nodes, get_in_time list, visited statuses and general time
n = int(input())
connections = [list() for i in range(n)]
get_in_time = [0 for i in range(n)]
visited_status = ['white' for i in range(n)]
hours = 0

# Filling connections list
for i in range(n - 1):
    a, b = list(map(int, input().split()))
    connections[a - 1].append(b - 1)
    connections[b - 1].append(a - 1)

# Calling DFS
dfs_algo(0)
print(sum(get_in_time))
