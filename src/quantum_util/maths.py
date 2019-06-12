from scipy.integrate import quad
from scipy import sin, pi
import numpy as np

def quadrant(x, y):
    return (0 if y >= 0 else 3) if x > 0 else (1 if y >= 0 else 2)


def complete_elliptic_pi(n, m):
    f = lambda x: 1 / sqrt(1 - m * sin(x) ** 2) * 1 / (1 - n * sin(x) ** 2)
    return quad(f, 0, pi / 2)[0]


def dots(*args):
    if len(args) < 2: return args
    out = dot(args[-2], args[-1])
    for m in reversed(args[:-2]): out = dot(m, out)
    return out

def ct(m): return np.conj(m.T)


