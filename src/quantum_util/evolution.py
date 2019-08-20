# Finite Time Evolution
# Code for time evolving a set of states. 

from scipy.linalg import expm
import numpy as np
from numpy import matmul, sqrt
def noop(*args, **kwargs):
    pass

class EvolvingState(np.ndarray):

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        obj._init_me()
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.evolve = getattr(obj, 'evolve', None)
    
    def _init_me(self):
        self.evolve = self._evolve_expm
        if len(self.shape) == 1:
            pass # expand shape to 2d
        
    def inormalize(self):
        self /= np.total(abs(self)**2, axis=0)
    
    def _evolve_lin(self, h, dt):
        self += 1.0j * dt * (h @ self)
        self.inormalize()
    
    def _evolve_expm(self, h, dt):
        self = EvolvingState(matmul(expm(1.0j * dt * h), self))
        
    @property
    def CT(self):
        return self.T.conj()
    
def evolve(ham_f, states, ts, precision=1.0e-10, callback=noop):
    # Evolve in the dumbest way possible.
    for n, t in enumerate(ts[:-1]):
        callback(n, t)
        states.evolve(ham_f(t), ts[n+1]-ts[n])

