import scipy as sp
import numpy as np
from scipy import array, pi, cos, exp, sin, arctan2, sqrt, dot, conj, log, diag, imag
from scipy.linalg import eigh, eigvalsh


def ipr(v, n=4):
    """
    Inverse participation ratio (Normalized)
    :param v: vector of dimension D
    :param n: ipr power. default 4
    :return: ipr ( number between 1/D and 1.0)
    """
    return sum(abs(v)**n)/sum(abs(v)**2)

def expect(v1, op, v2):
    return dot(conj(v1), dot(op, v2))

def groundstate(h):
    return eigh(h)[1][:, 0]

def com(v):
    """
    Normalized center of mass.
    :param v: vector in configuration space
    :return: com (scalar between -0.5 and 0.5)
    """
    return np.dot(abs(v)**2, np.arange(len(v)))/len(v) - 1/2

