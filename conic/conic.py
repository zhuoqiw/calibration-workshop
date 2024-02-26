import numpy as np

class Conic:
    def __init__(self, A, B, C, D, E, F) -> None:
            self.fromQuadric(A, B, C, D, E, F)

    def fromQuadric(self, A, B, C, D, E, F):
        self.m = np.array([[A, B / 2, D / 2], [B / 2, C, E / 2], [D / 2, E / 2, F]])

    def toQuadric(self):
        m = self.m
        return (m[0, 0], m[0, 1] * 2, m[1, 1], m[0, 2] * 2, m[1, 2] * 2, m[2, 2])

    def Q(self, x, y):
        A, B, C, D, E, F = self.getQuadric()
        return A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F
    
    def getQuadric(self):
        m = self.m
        # A = m[0, 0]
        # B = m[0, 1] * 2
        # C = m[1, 1]
        # D = m[0, 2] * 2
        # E = m[1, 2] * 2
        # F = m[2, 2]
        return (m[0, 0], m[0, 1] * 2, m[1, 1], m[0, 2] * 2, m[1, 2] * 2, m[2, 2])

    def discriminant(self):
        A = self.m[0, 0]
        B = self.m[0, 1] * 2
        C = self.m[1, 1]
        return B ** 2 - 4 * A * C

    def perspectiveTransform(self, H):
        Hinv = np.linalg.inv(H)
        self.m = Hinv.T @ self.m @ Hinv

    def isEllipse(self):
        if self.discriminant() < 0:
            return True
        else:
            return False

    def isCircle(self):
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