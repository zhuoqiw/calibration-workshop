from collections import namedtuple
import numpy as np
from . import ellipse

class Conic(namedtuple("ConicBase", "A, B, C, D, E, F")):
    """A namedtuple to represent a conic section."""
    @property
    def dis(self):
        A, B, C, *t = self
        return B ** 2 - 4 * A * C
    
    @property
    def det(self):
        return np.linalg.det(self.m)

    @property
    def m(self):
        A, B, C, D, E, F = self
        return np.array([[A, B / 2, D / 2], [B / 2, C, E / 2], [D / 2, E / 2, F]])
    
    @property
    def ellipse(self):
        if not self.is_ellipse():
            return None
        A, B, C, D, E, F = self
        d = self.dis
        a = -np.sqrt(2 * (A * E ** 2 + C * D ** 2 - B * D * E + d * F) * (A + C + np.sqrt((A - C) ** 2 + B ** 2))) / d
        b = -np.sqrt(2 * (A * E ** 2 + C * D ** 2 - B * D * E + d * F) * (A + C - np.sqrt((A - C) ** 2 + B ** 2))) / d
        x = (2 * C * D - B * E) / d
        y = (2 * A * E - B * D) / d
        r = np.arctan2(-B, C - A) / 2
        return ellipse.Ellipse(x, y, a, b, r)
        
    def __call__(self, x, y):
        A, B, C, D, E, F = self
        return A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F

    def __rmatmul__(self, H):
        _H = np.linalg.inv(H)
        _M = _H.T @ self.m @ _H
        assert(np.array_equal(_M, _M.T))
        return Conic(_M[0, 0], _M[0, 1] * 2, _M[1, 1], _M[0, 2] * 2, _M[1, 2] * 2, _M[2, 2])

    def is_degenerate(self):
        return True if self.det == 0 or self.det * self.C > 0 else False
    
    def is_ellipse(self):
        return True if self.dis < 0 and self.C * self.det <= 0 else False

    def is_circle(self):
        if not self.is_ellipse():
            return False
        A, B, C, *t = self
        return True if B == 0 and A == C != 0 else False

    def is_parabola(self):
        return True if self.dis == 0 else False

    def is_hyperbola(self):
        return True if self.dis > 0 else False
        
    def is_rectangular(self):
        if not self.is_hyperbola():
            return False
        A, B, C, *t = self
        return True if A + C == 0 else False