import scipy as sp
import numpy as np
from scipy import array, pi, cos, exp, sin, arctan2, sqrt, dot, conj, log, diag, imag
from scipy.linalg import eigh, eigvalsh


def ipr(v,n=4):
    return sum(abs(v)**n)/sum(abs(v)**2)

def expect(v1, op, v2):
    return dot(conj(v1), dot(op, v2))

def groundstate(h):
    return eigh(h)[1][:, 0]

def com(v): 
    return np.dot(abs(v)**2, np.arange(len(v)))/len(v) - 1/2

