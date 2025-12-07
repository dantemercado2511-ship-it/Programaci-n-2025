import numpy as np
from bisection import bisection
import time

error = 1e-10

def f(x,a):
    return x**2 - a
def df(x):
    return 2*x


def sqrt_bisection(a):
    """
    returns the square root of a, calculated by the bisection method
    """
    def f(x):
        return x**2 - a

    if a == 0:
        return 0
    elif a > 0:
        interval = [0,a]
    elif a < 0:
        interval = [a,0]

    return bisection(f,interval,error = error,show=True)

def sqrt_newtonRaphson(a):
    """
    returns the square root of a, calculated by the Newton - Raphson method
    """
    r = 3
    if a == 0:
        return 0

    x = a
    h = f(x,r) / df(x)
    count = 0
    while abs(h) > error:
        count += 1
        h = f(x,r) / df(x)
        x = x - h
    print(f'iterations={count}')
    return x

a = 3

print('Bisection Method:')
start = time.time()
x = sqrt_bisection(a)
end = time.time()
print(x)
print(f'elapsed time: {end-start}s')

print()
print('Newton - Raphson Method:')
start = time.time()
x = sqrt_newtonRaphson(a)
end = time.time()
print(x)
print(f'elapsed time: {end-start}s')
