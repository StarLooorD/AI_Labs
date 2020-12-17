# DFS algorithm
def dfs(node, ancestor, start_cage):
    global is_cycle
    # Setting current node to visited
    visited[node] = True
    # Getting through all connections of this node
    for child in connections[node]:
        # Passing if connection is actually father
        if child == ancestor:
            continue
        # If we returned to start node we found a cycle
        if child == start_cage:
            is_cycle = True
            return
        # If current child is not in visited list continue doing DFS
        if not visited[child]:
            dfs(child, node, start_cage)


# Inputting number of cages (nodes) and tubes (edges)
cages, tubes = map(int, input().split())
# Setting:
# connections - for all connections between nodes
connections = [[] for i in range(100)]
# nodes_in_cycle - counter of nodes which are in cycle
nodes_in_cycle = []
# is_cycle - boolean variable for defining cycle
is_cycle = False

# Filling connections list
for i in range(tubes):
    a, b = map(int, input().split())
    connections[a - 1].append(b - 1)
    connections[b - 1].append(a - 1)
# For each cage (as start point) calling DFS
for node_number in range(cages):
    # Visited - list where we can see whether was cage visited or not
    visited = [False] * cages
    dfs(node_number, -1, node_number)
    if is_cycle:
        nodes_in_cycle.append(node_number + 1)
# Checking if cycle contains at least 1 node and print min value of it
if len(nodes_in_cycle) > 0:
    print(min(nodes_in_cycle))
# Otherwise print -1
else:
    print(-1)
