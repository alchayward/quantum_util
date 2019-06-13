from scipy.sparse.linalg import LinearOperator
import numpy as np
from quantum_util.maths import ct
from quantum_util.misc import Compatibility


class Operator(LinearOperator):

    def __init__(self, shape, **kwargs):
        super().__init__(shape, **kwargs)

    def check_compatible(self, op):
        compatible = Compatibility([lambda: self.shape[1] == op.shape[0]])
        return compatible.check()

    def compose(self, op):
        def matvec(x): return self(op(x))

        def matmat(m): return self(op(m))

        return Operator(shape=(self.shape[0], op.shape[1]), matvec=matvec, matmat=matmat, dtype=self.dtype)


class Commutator(Operator):

    def __init__(self, a, b, **kwargs):
        assert a.check_compatible(b) and b.check_compatible(a)
        self._a, self._b = a, b
        super().__init__(a.shape, **kwargs)

    def __call__(self, v):
        out = self._a(self._b(v))
        out -= self._b(self._a(out))
        return out


class ParameterizedOperator(Operator):

    def __init__(self, shape, params, func, **kwargs):
        """
            func should return an Operator
        """
        self._params = params
        self._func = func
        super().__init__(shape, **kwargs)

    def __call__(self, *params):
        return self._func(*params)


class ParameterizedHamiltonian(ParameterizedOperator):

    def get_param_wavefunction(self, n=0):
        def wf(*args):
            h = self._func(*args)
            e, v = np.linalg.eigh(h)
            return e[n], v[:, n]

        return ParameterizedWavefunction(self.shape[0],
                                         self._params, wf, self.dtype)


class Wavefunction(np.ndarray):

    def overlap(self, wf):
        return np.dot(ct(self), wf)


class ParameterizedWavefunction(Wavefunction):

    def __init__(self, dimension, params, func, dtype):
        self._func = func
        self.shape = (dimension,)
        self.dtype = dtype
        self.params = params

    def __call__(self, *args):
        return self._func(*args)[1]
