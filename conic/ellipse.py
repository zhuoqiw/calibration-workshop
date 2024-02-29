from collections import namedtuple
import numpy as np
from .conic import Conic

class Ellipse(namedtuple("EllipseBase", "x, y, a, b, r")):
    """A namedtuple to represent an ellipse."""
    @property
    def conic(self):
        x, y, a, b, r = self
        sin = np.sin(r)
        cos = np.cos(r)
        A = a ** 2 * sin ** 2 + b ** 2 * cos ** 2
        B = 2 * (b ** 2 - a ** 2) * sin * cos
        C = a ** 2 * cos ** 2 + b ** 2 * sin ** 2
        D = -2 * A * x - B * y
        E = -2 * C * y - B * x
        F = A * x ** 2 + B * x * y + C * y ** 2 - a ** 2 * b ** 2
        return Conic(A, B, C, D, E, F)

    # def fromConic(self):
    #     A, B, C, D, E, F = self.quadratic()
    #     dis = self.discriminant()
    #     a = -np.sqrt(2 * (A * E ** 2 + C * D ** 2 - B * D * E + dis * F) * (A + C + np.sqrt((A - C) ** 2 + B ** 2))) / dis
    #     b = -np.sqrt(2 * (A * E ** 2 + C * D ** 2 - B * D * E + dis * F) * (A + C - np.sqrt((A - C) ** 2 + B ** 2))) / dis
    #     x = (2 * C * D - B * E) / dis
    #     y = (2 * A * E - B * D) / dis
    #     if B == 0:
    #         if A <= C:
    #             radian = 0
    #         else:
    #             radian = np.pi / 2
    #     else:
    #         radian = np.arctan((C - A - np.sqrt((A - C) ** 2 + B ** 2)) / B)
    #     self._center = (x, y)
    #     self._axes = (a, b)
    #     self._radian = radian

    # def limits(self):
    #     sin = np.sin(self._radian)
    #     cos = np.cos(self._radian)
    #     src = np.array(
    #         [
    #             [[+self._axes[0], 0]],
    #             [[-self._axes[0], 0]],
    #             [[0, +self._axes[1]]],
    #             [[0, -self._axes[1]]]
    #         ], float)
    #     m = np.array(
    #         [
    #             [cos, -sin, self._center[0]],
    #             [sin, +cos, self._center[1]]
    #         ], float)
    #     dst = cv.transform(src, m)
    #     return np.min(dst[..., 0]), np.max(dst[..., 0]), np.min(dst[..., 1]), np.max(dst[..., 1])

    # def draw(self, *, ax=None):
    #     if ax is None:
    #         ax = plt.gca()
        
    #     xcenter, ycenter = self._center
    #     a, b = self._axes
    #     angle = -30
    #     theta = np.deg2rad(np.arange(0.0, 360.0, 1.0))
    #     x = a * np.cos(theta)
    #     y = b * np.sin(theta)

    #     rtheta = self._radian
    #     R = np.array([
    #         [np.cos(rtheta), -np.sin(rtheta)],
    #         [np.sin(rtheta),  np.cos(rtheta)],
    #         ])

    #     x, y = np.dot(R, [x, y])
    #     x += xcenter
    #     y += ycenter

    #     ax.fill(x, y, alpha=0.2, facecolor='yellow', edgecolor='yellow', linewidth=1, zorder=1)

# def unbiasedCenterImpl(objectPoints, rvec, tvec, cameraMatrix, radius):
#     objectPoints = np.asarray(objectPoints, float).reshape(-1, 1, 3)
#     rvec = np.asarray(rvec, float).reshape(3)
#     tvec = np.asarray(tvec, float).reshape(3)
#     cameraMatrix = np.asarray(cameraMatrix, float).reshape(3, 3)

#     H, j = cv.Rodrigues(rvec)
#     H[:, 2] = tvec
#     H = cameraMatrix @ H
#     Hinv = np.linalg.inv(H)
#     imagePoints, j = cv.projectPoints(objectPoints, rvec, tvec, cameraMatrix, None)
#     ret = []
#     for [obj], [img] in zip(objectPoints, imagePoints):
#         A = 1
#         B = 0
#         C = 1
#         D = obj[0] * -2
#         E = obj[1] * -2
#         F = obj[0] ** 2 + obj[1] ** 2 - radius ** 2
#         Aq = np.array([[A, B / 2, D / 2], [B / 2, C, E / 2], [D / 2, E / 2, F]], float)
#         Aq = Hinv.T @ Aq @ Hinv
#         A = Aq[0, 0]
#         B = Aq[0, 1] * 2
#         C = Aq[1, 1]
#         D = Aq[0, 2] * 2
#         E = Aq[1, 2] * 2
#         F = Aq[2, 2]
#         xc = (B * E - 2 * C * D) / (4 * A * C - B ** 2)
#         yc = (D * B - 2 * A * E) / (4 * A * C - B ** 2)
#         ret.append([img[0] - xc, img[1] - yc])
#     return np.array(ret, float).reshape(-1, 1, 2)