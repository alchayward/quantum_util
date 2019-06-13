from scipy.sparse.linalg import LinearOperator

class Operator(LinearOperator):

    #def __init__(self, shape, **kwargs):
    #    super.__init__(shape, **kwargs)

    def __call__(self, vec):
        return self.matvec(vec)

    def check_compatible(self, op):
        self.shape[1] == op.shape[0]

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
    pass
