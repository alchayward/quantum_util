# tools for analysing topologial quantities for various systems
import numpy as np
from scipy.integrate import quad, dblquad
from scipy import pi, log, imag
from quantum_util.operators import ParameterizedWavefunction
# 1D topology

def polarization(wf, d_phi=1.0e-10):
    """
        todo:
            have a more sofisticated (adaptive) mesh
    """
    def bp(phi):
        return imag(log( wf(phi).overlap(wf(phi+d_phi))))/d_phi
    return quad(bp, 0, 2*pi)[0]

# 2D topology

def berry_curvature(wf, phi_x, phi_y, d_phi=1.0e-10):
    return imag(log(dot(wf(phi), wf(phi+d_phi))))/d_phi

def chern_number(wf, d_phi=1.0e-10):

    def bc(x, y):
        return berry_curvature(wf, x, y, d_phi)
    
    return dblquad(bc, 0, 2 * pi, lambda x: 0.0, lambda x: 2 * pi)[0]
