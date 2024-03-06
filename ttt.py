import conic
import numpy as np

x = 10
y = 10
a = 1
b = 1
A = 1 / a
B = 0
C = 1 / b
D = 2 * x / a
E = 2 * y / b
F = x ** 2 / a + y ** 2 / b

c1 = conic.Conic(1, 0, 1, 2, -2, 2)

print(c1.ellipse)