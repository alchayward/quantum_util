# tools for analysing topologial quantities for various systems
import numpy as np
from scipy.integrate import quad, dblquad
from scipy import pi, log, imag
from quantum_util.operators import ParameterizedWavefunction
# 1D topology

class TorusState2D(object):

    """Docstring for TorusState2D. 
        Todo: Add some memorization and/or interpolation
    """

    def __init__(self, state_fun, shape=None, ham_f=None):
        """TODO: to be defined1. """
        self._state_f = state_fun
        self.shape  = shape if shape is not None else state_fun(0,0).shape
        self.ham_f  = ham_f 


    def __call__(self, theta_x, theta_y):
        return self.state_f(theta_x, theta_y)
 
    def chern_number():
        

class TorusState1D(object):

    """Docstring for TorusState. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    def __call__(self, theta_x):
        pass

def polarization(wf, d_phi=1.0e-10):
    """
    Polarization from Resta formula.
    """
    L = states.shape[0]
    X = diag(exp(-1.0j*linspace(0,2*pi,L)))
    return -imag(log(det(conj(states.T) @ X @ states)))
 

def integrate_d_pol(pol, max_d = .1):
    diffs = imag(log(exp(1.0j*(pol[1:] - pol[:-1])))) 
    cum = np.cumsum([x if abs(x) < max_d else 0.0 for x in diffs ])
    return np.concatenate((np.array([0]), cum))

# Where do these differ. And why does one involve inverting the state. 
def current_dP(states, ham):
    L = states.shape[0]
    X = diag(exp(-1.0j*linspace(0, 2*pi,L)))
    eX =  conj(states.T) @ X @ states
    dX = conj(states.T) @ ((X @ ham) - (ham @ X)) @ states
    return 1.0j*trace(np.linalg.inv(eX) @ dX)

## Derivitive with respect to potential
def current_dphi(states, ham_f,d_phi= 1.0e-7, phi_0=0.0):
    dh = ham_f(phi_0+d_phi) - ham_f(phi_0)
    return -2*np.real(trace(conj(states.T) @ (dh) @ states)/d_phi)/(2*pi)

def curvature(psi_f):


def integrated_current():
    pass
        
# 2D topology

def curvature_fukuie():
    pass

def berry_curvature(wf, phi_x, phi_y, d_phi=1.0e-10):
    return imag(log(dot(wf(phi), wf(phi+d_phi))))/d_phi

def chern_number(wf, d_phi=1.0e-10):

    def bc(x, y):
        return berry_curvature(wf, x, y, d_phi)
    
    return dblquad(bc, 0, 2 * pi, lambda x: 0.0, lambda x: 2 * pi)[0]
