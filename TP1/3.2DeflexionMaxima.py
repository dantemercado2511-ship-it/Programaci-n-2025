from bisection import bisection

L=600
E=50e3
I=30e3
w=2.5

def f(x):
    return (w / (120 * E * I * L)) * (-(x**5) + 2 * L**2 * x**3 - L**4 *x)

def df(x):
    return (w / (120 * E * I * L)) * (-5*(x**4) + 6 * L**2 * x**2 - L**4)

max_def = bisection(df,[1,599])#No puedo usar 0 y 600 porque son raices

print(f'Punto de deflexión máxima: {max_def}')
print(f'Valor de deflexión máxima: {f(max_def)}')
