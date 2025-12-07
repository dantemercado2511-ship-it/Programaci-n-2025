from bisection import bisection

def f(y):
    Q = 20
    g = 9.81

    def B(y):
        return 3 + y

    def Ac(y):
        return 3*y + (y**2 / 2)

    return 1 - Q**2 / (g * Ac(y)**3) * B(y)

print(bisection(f, [1, 2], error = 1e-9, max_iterations = 10, show=True))

