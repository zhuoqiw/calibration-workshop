from collections import namedtuple
import numpy as np


class Conic(namedtuple("ConicBase", "A, B, C, D, E, F")):
    """A namedtuple to represent a conic section."""
    @property
    def discriminant(self):
        A, B, C, *t = self
        return B ** 2 - 4 * A * C
    
    def fn(self, x, y):
        A, B, C, D, E, F = self
        return A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F

    def transform(self, M):
        invM = np.linalg.inv(M)
        m = invM.T @ self._m @ invM
        return Conic(m[0, 0], m[0, 1] * 2, m[1, 1], m[0, 2] * 2, m[1, 2] * 2, m[2, 2])

    def isEllipse(self):
        if self.discriminant() < 0:
            return True
        else:
            return False

    def isCircle(self):
        if not self.isEllipse():
            return False
        A, B, C, *t = self.getQuadric()
        if B == 0 and A == C != 0:
            return True
        else:
            return False

    def isParabola(self):
        if self.discriminant() == 0:
            return True
        else:
            return False

    def isHyperbola(self):
        if self.discriminant() > 0:
            return True
        else:
            return False
        
    def isRectangular(self):
        if not self.isHyperbola():
            return False
        A, B, C, *t = self.getQuadric()
        if A + C == 0:
            return True
        else:
            return False
        
    def draw(self):
        pass

c = Conic(1, 2, 3, 4, 5, 6)

print(c.discriminant)