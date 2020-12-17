def dfs_search_cycle(node, pr_node, color, is_in_cycle, ancestor):

    if color[node] == 'black':
        return None

    elif color[node] == 'grey':
        current = pr_node
        is_in_cycle[current] = True
        while current != node:
            current = ancestor[current]
            is_in_cycle[current] = True
        return None

    else:
        ancestor[node] = pr_node
        color[node] = 'grey'

        for connection in connections[node]:
            if connection == ancestor[node]:
                continue
            dfs_search_cycle(connection, node, color, is_in_cycle, ancestor)

        color[node] = 'black'


n = int(input())

connections = [[] for i in range(n + 1)]

for i in range(n):
    p, q = map(int, input().split())
    connections[p].append(q)
    connections[q].append(p)

color = ['white'] * (n + 1)
ancestor = [0] * (n + 1)
is_in_cycle = [False] * (n + 1)

dfs_search_cycle(1, 0, color, is_in_cycle, ancestor)

res = [i for i in range(n + 1) if is_in_cycle[i] != 0]
print(len(res))
print(*res)
