def main():
    n = int(input())
    lines = []

    for i in range(n):
        x0, y0, z0, x1, y1, z1 = [int(xx) for xx in input().split()]
        lines.append(((x0, y0, z0), (x1, y1, z1)))

    x_prev, y_prev, z_prev = 1.0, 1.0, 1.0
    x, y, z = 0.0, 0.0, 0.0
    eps = 0.000001
    step = 1.0

    while abs(x_prev - x) + abs(y_prev - y) + abs(z_prev - z) > eps:
        x_prev, y_prev, z_prev = x, y, z
        x = x_prev - step * deriv('x', n, lines, x_prev, y_prev, z_prev)
        y = y_prev - step * deriv('y', n, lines, x_prev, y_prev, z_prev)
        z = z_prev - step * deriv('z', n, lines, x_prev, y_prev, z_prev)

        if func(n, lines, x, y, z) > func(n, lines, x_prev, y_prev, z_prev):
            step /= 2

    print(func(n, lines, x, y, z))


def func(n, lines, x, y, z):
    res = 0
    for i in range(n):
        line_i = lines[i]
        case_i = get_case(line_i, x, y, z)
        x0, y0, z0 = line_i[0][0], line_i[0][1], line_i[0][2]
        x1, y1, z1 = line_i[1][0], line_i[1][1], line_i[1][2]
        if case_i == 1:
            res += dots_dist(x, y, z, x1, y1, z1)
        elif case_i == 2:
            res += dots_dist(x, y, z, x0, y0, z0)
        else:
            res += dot_line_dist(line_i, x, y, z)
    return res


def deriv(var, n, lines, x, y, z):
    res = 0
    for i in range(n):
        line_i = lines[i]
        case_i = get_case(line_i, x, y, z)
        x0, y0, z0 = line_i[0][0], line_i[0][1], line_i[0][2]
        x1, y1, z1 = line_i[1][0], line_i[1][1], line_i[1][2]
        if case_i == 1:
            res += dots_deriv(var, x1, y1, z1, x, y, z)
        elif case_i == 2:
            res += dots_deriv(var, x0, y0, z0, x, y, z)
        else:
            res += dot_line_deriv(var, line_i, x, y, z)
    return res


def get_case(line, x, y, z):
    a = line[1][0] - line[0][0]
    b = line[1][1] - line[0][1]
    c = line[1][2] - line[0][2]
    AB = (a, b, c)
    a = x - line[1][0]
    b = y - line[1][1]
    c = z - line[1][2]
    BE = (a, b, c)
    a = x - line[0][0]
    b = y - line[0][1]
    c = z - line[0][2]
    AE = (a, b, c)
    AB_BE = AB[0] * BE[0] + AB[1] * BE[1] + AB[2] * BE[2]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1] + AB[2] * AE[2]
    if AB_BE > 0:
        res = 1
    elif AB_AE < 0:
        res = 2
    else:
        res = 3
    return res


def dots_dist(x0, y0, z0, x1, y1, z1):
    res = ((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)**0.5
    return res


def dots_deriv(var, x1, y1, z1, x, y, z):
    f = dots_dist(x1, y1, z1, x, y, z)
    if var == 'x':
        res = (x - x1) / f
    elif var == 'y':
        res = (y - y1) / f
    elif var == 'z':
        res = (z - z1) / f
    return res


def dot_line_dist(line, x, y, z):
    x0, y0, z0 = line[0][0], line[0][1], line[0][2]
    x1, y1, z1 = line[1][0], line[1][1], line[1][2]
    vi = (y1 - y0) * (z - z0) - (z1 - z0) * (y - y0)
    vj = (z1 - z0) * (x - x0) - (x1 - x0) * (z - z0)
    vk = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)
    mod = ((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)**0.5
    vlen = (vi**2 + vj**2 + vk**2)**0.5
    f = vlen / mod
    return f


def dot_line_deriv(var, line, x, y, z):
    x0, y0, z0 = line[0][0], line[0][1], line[0][2]
    x1, y1, z1 = line[1][0], line[1][1], line[1][2]
    vi = (y1 - y0) * (z - z0) - (z1 - z0) * (y - y0)
    vj = (z1 - z0) * (x - x0) - (x1 - x0) * (z - z0)
    vk = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)
    mod = ((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)**0.5
    vlen = (vi**2 + vj**2 + vk**2)**0.5
    if var == 'x':
        res = (vj * (z1 - z0) + vk * (y0 - y1)) / (mod * vlen)
    elif var == 'y':
        res = (vi * (z0 - z1) + vk * (x1 - x0)) / (mod * vlen)
    elif var == 'z':
        res = (vi * (y1 - y0) + vj * (x0 - x1)) / (mod * vlen)
    return res



main()