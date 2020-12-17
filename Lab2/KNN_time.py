def distance(x, y):
    return max(abs(x[0]-y[0]), abs(x[1] - y[1]))


def find_closest(set, item, classes, k):
    distances = [(distance(set[letter], item), i) for i, _class in enumerate(classes.values())
                 for letter in _class[:_class.index(-1)]]
    distances.sort(key=lambda x: x[0])
    if len(distances) <= k:
        return distances
    else:
        amount = k
        while True and amount < len(distances):
            if distances[amount - 1][0] == distances[amount][0]:
                amount += 1
            else:
                break
        return distances[:amount]


n, k, m = list(map(int, input().split()))
classes = [tuple(map(int, input().split())) for _ in range(n)]
to_classify = [tuple(map(int, input().split())) for _ in range(m)]
all_letter = classes + to_classify

class_letters = {i: [i] + [-1] * (1000 - n) for i in range(n)}

for j, letter in enumerate(to_classify):
    classes_count = {i: 0 for i in range(n)}
    all_distances = find_closest(all_letter, letter, class_letters, k)
    for d in all_distances:
        classes_count[d[1]] += 1
    _max_class = max(classes_count, key=classes_count.get)
    class_letters[_max_class][class_letters[_max_class].index(-1)] = j + n
    print(_max_class + 1, end=' ')
