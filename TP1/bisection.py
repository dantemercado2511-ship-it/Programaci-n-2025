import numpy as np

def bisection(f,interval,error = 1e-6, max_iterations = 100, show = False, return_iterations = False):
    """
    Find a root of f within a given interval using the bisection method.

    Parameters
    ----------
    f : callable
        Function for which the root is sought. must return a number.
    interval : list of float
        Two-element list [a, b] defining the search interval.
    error : float, optional
        Desired tolerance for the root approximation (default is 1e-6).
    max_iterations : int, optional
        Maximum number of iterations (default is 100).

    Returns
    -------
    float
        Approximated root of the function within the interval.
    """
    if not isinstance(interval,list):
        raise ValueError('interval must be a list')

    if not len(interval) == 2:
        raise ValueError('interval must have 2 items')

    if not callable(f):
        raise ValueError('f must be callable')

    if not isinstance(f(interval[0]),(float, int)):
        raise ValueError('f must return a number')

    x=0

    for count in range(max_iterations):
        left = f(interval[0])
        right = f(interval[1])

        if left*right < 0:
            x = (interval[0]+interval[1])/2
            y = f(x)
            if abs(y) < error:
                break
            elif y > 0:
                interval[1] = x
            elif y < 0:
                interval[0] = x
        else:
            raise ValueError('No roots within the interval')

    if show:
        print(f'epsilon={interval[1]-interval[0]}')
        print(f'iterations={count}')

    if return_iterations:
        return (x,count)
    else:
        return x
