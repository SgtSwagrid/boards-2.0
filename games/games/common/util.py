import math


def is_orthogonal(x_from, y_from, x_to, y_to):

    return (x_to - x_from != 0) ^ (y_to - y_from != 0)

def is_diagonal(x_from, y_from, x_to, y_to):

    return abs(x_to - x_from) == abs(y_to - y_from) != 0

def is_line(x_from, y_from, x_to, y_to):

    return is_orthogonal(x_from, y_from, x_to, y_to) or\
        is_diagonal(x_from, y_from, x_to, y_to)

def direction(x_from, y_from, x_to, y_to):

    if x_to == x_from and y_to == y_from: return 0, 0
    gcd = math.gcd(x_to - x_from, y_to - y_from)
    return (x_to - x_from) // gcd, (y_to - y_from) // gcd

def steps(x_from, y_from, x_to, y_to):

    dx, dy = direction(x_from, y_from, x_to, y_to)
    if dx == dy == 0: return 0
    elif dy == 0: return (x_to - x_from) // dx
    else: return (y_to - y_from) // dy
