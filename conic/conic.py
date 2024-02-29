from collections import namedtuple
import numpy as np

class Conic(namedtuple("ConicBase", "A, B, C, D, E, F")):
    """A namedtuple to represent a conic section."""
    @property
    def d(self):
        A, B, C, *t = self
        return B ** 2 - 4 * A * C

    @property
    def m(self):
        A, B, C, D, E, F = self
        return np.array([[A, B / 2, D / 2], [B / 2, C, E / 2], [D / 2, E / 2, F]])

    def __call__(self, x, y):
        A, B, C, D, E, F = self
        return A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F

    def __rmatmul__(self, H):
        _H = np.linalg.inv(H)
        _M = _H.T @ self.m @ _H
        assert(np.array_equal(_M, _M.T))
        return Conic(_M[0, 0], _M[0, 1] * 2, _M[1, 1], _M[0, 2] * 2, _M[1, 2] * 2, _M[2, 2])

    def is_ellipse(self):
        if self.d() < 0:
            return True
        else:
            return False

    def is_circle(self):
        if not self.is_ellipse():
            return False
        A, B, C, *t = self
        if B == 0 and A == C != 0:
            return True
        else:
            return False

    def is_parabola(self):
        if self.d() == 0:
            return True
        else:
            return False

    def is_hyperbola(self):
        if self.d() > 0:
            return True
        else:
            return False
        
    def is_rectangular(self):
        if not self.is_hyperbola():
            return False
        A, B, C, *t = self
        if A + C == 0:
            return True
        else:
            return False