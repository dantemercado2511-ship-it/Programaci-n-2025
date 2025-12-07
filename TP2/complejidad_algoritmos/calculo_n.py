import math

def calcular_n(T: callable, operaciones: int) -> int:
    n = 1
    while T(n) < operaciones:
        n += 1
    return n - 1

if __name__ == '__main__':
    op = 1e6

    def T1(n):
        return n * math.log10(n)

    def T2(n):
        return math.factorial(n)

    print(calcular_n(T1,op))
    print(calcular_n(T2,op))
