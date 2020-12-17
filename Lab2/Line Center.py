import math

N = int(input())
accuracy = 0.00001


def euclid_distance(current_point, start_or_end):
    return ((current_point[0] - start_or_end[0]) ** 2 + (current_point[1] - start_or_end[1]) ** 2
            + (current_point[2] - start_or_end[2]) ** 2) ** 0.5


def func(current_point, start, end):
    min_dist = 0
    for i in range(len(start)):
        from_dot_to_start = euclid_distance(current_point, start[i])
        from_dot_to_end = euclid_distance(current_point, end[i])
        from_start_to_end = euclid_distance(start[i], end[i])
        # first situation
        if (from_dot_to_start == (from_dot_to_end + from_start_to_end)) or (
                from_dot_to_end == (from_dot_to_start + from_start_to_end)):
            min_dist += min(from_dot_to_start, from_dot_to_end)
            continue
        # second situation
        cos_alpya = (from_dot_to_start ** 2 + from_start_to_end ** 2 - from_dot_to_end ** 2) / (
                2 * from_dot_to_start * from_start_to_end)
        cos_beta = (from_dot_to_end ** 2 + from_start_to_end ** 2 - from_dot_to_start ** 2) / (
                2 * from_dot_to_end * from_start_to_end)
        if cos_alpya < 0 or cos_beta < 0:
            min_dist += min(from_dot_to_start, from_dot_to_end)
            continue
        # third situation
        p = (from_dot_to_start + from_dot_to_end + from_start_to_end) / 2
        S = (p * (p - from_dot_to_start) * (p - from_dot_to_end) * (p - from_start_to_end)) ** 0.5
        h = (2 * S) / from_start_to_end
        min_dist += h
        # s_vector = [end[i][0] - start[i][0], end[i][1] - start[i][1], end[i][2] - start[i][2]]
        # M0_M1 = [start[i][0] - current_point[0], start[i][1] - current_point[1], start[i][2] - current_point[2]]
        # M0_M1_x_S = [M0_M1[1] * s_vector[2] - M0_M1[2] * s_vector[1],
        #              -(M0_M1[0] * s_vector[2] - M0_M1[2] * s_vector[0]),
        #              M0_M1[0] * s_vector[1] - M0_M1[1] * s_vector[0]]
        # min_dist += (M0_M1_x_S[0] ** 2 + M0_M1_x_S[1] ** 2 + M0_M1_x_S[2] ** 2) ** 0.5 / (
        #         s_vector[0] ** 2 + s_vector[1] ** 2 + s_vector[2] ** 2) ** 0.5
    return min_dist


def main():
    start = []
    end = []
    for i in range(N):
        x1, y1, z1, x2, y2, z2 = map(int, input().split())
        start.append([x1, y1, z1])
        end.append([x2, y2, z2])

    distance_to_add = 100
    current_point = [0, 0, 0]
    min_dist = 10000000
    while accuracy < distance_to_add:
        current_point[0] += distance_to_add
        changed_distance = func(current_point, start, end)
        if changed_distance < min_dist:
            min_dist = changed_distance
            continue
        else:
            current_point[0] -= distance_to_add

        current_point[0] -= distance_to_add
        changed_distance = func(current_point, start, end)
        if changed_distance < min_dist:
            min_dist = changed_distance
            continue
        else:
            current_point[0] += distance_to_add

        current_point[1] += distance_to_add
        changed_distance = func(current_point, start, end)
        if changed_distance < min_dist:
            min_dist = changed_distance
            continue
        else:
            current_point[1] -= distance_to_add

        current_point[1] -= distance_to_add
        changed_distance = func(current_point, start, end)
        if changed_distance < min_dist:
            min_dist = changed_distance
            continue
        else:
            current_point[1] += distance_to_add

        current_point[2] += distance_to_add
        changed_distance = func(current_point, start, end)
        if changed_distance < min_dist:
            min_dist = changed_distance
            continue
        else:
            current_point[2] -= distance_to_add

        current_point[2] -= distance_to_add
        changed_distance = func(current_point, start, end)
        if changed_distance < min_dist:
            min_dist = changed_distance
            continue
        else:
            current_point[2] += distance_to_add

        distance_to_add = distance_to_add / 2

    print(min_dist)


main()
