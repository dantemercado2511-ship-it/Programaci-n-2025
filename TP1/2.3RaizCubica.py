import numpy as np
from bisection import bisection

def cubeRoot(a):
    """
    returns the cube root of a, calculated by the bisection method
    """
    def f(x):
        return x**3 - a

    if a == 0:
        return 0
    elif a > 0:
        interval = [0,a]
    elif a < 0:
        interval = [a,0]

    return bisection(f,interval,error = 1e-10,show=True)


print(cubeRoot(-3))

