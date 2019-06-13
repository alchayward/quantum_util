# tools for analysing topologial quantities for various systems
import numpy as np
from scipy.integrate import quad
from scipy import pi, log, imag


# 1D topology

class ParameterizedHamiltonian:

    def __init__(self, func, shape, dtype, num_params, param_names=None):
        self.shape = shape
        self.num_params = num_params
        self.param_names = params
        self._func = func
        self.dtype = dtype

    def __call__(self, *args):
        return self._func(*args)

    def get_param_wavefunction(n=0):

        def wf(*args):
            h = self.func(*args)
            e, v = np.linalg.eigh(h)
            return e[n], v[:,n]
        
        return ParameterizedWavefunction(wf, self.shape[0], self.dtype)
 
class ParameterizedWavefunction:

    def __init__(self, func, dimension, dtype):
        self._func = func
        self.shape = dimension
        self.dtype = dtype

    def __call__(self, *args):
        return self._func(*args)[1]


def polarization(wf, d_phi):
    """
        todo:
            have a more sofisticated (adaptive) mesh
    """
    def bp(phi):
        return imag(log(dot(wf(phi).conj(), wf(phi+d_phi))))/d_phi
    quad(bp, 0, 2*pi)[0]
