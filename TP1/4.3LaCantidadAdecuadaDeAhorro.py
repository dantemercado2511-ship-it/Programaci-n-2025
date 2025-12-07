from bisection import bisection

salario_anual = float(input('Introduzca su salario anual: '))
costo_total = 1_000_000
aumento_semi_anual = 0.07
parte_pago_inicial = 0.25
pago_inicial = costo_total * parte_pago_inicial
ahorro_actual = 0.0
r = 0.04
salario_mensual = salario_anual / 12

def calcularAhorro(parte_ahorrada):
    salario = salario_mensual
    ahorro_actual = 0.0
    meses = 0
    while True:
        ahorro_actual *= 1 + r/12
        ahorro_actual += salario * parte_ahorrada
        meses += 1
        if meses % 6 == 0:
            salario *= 1 + aumento_semi_anual
        if meses == 36:
            break
    return ahorro_actual - pago_inicial

if calcularAhorro(1) < 0:
    print('No es posible el pago total en 3 años')
else:
    root = bisection(calcularAhorro,[0,1], error = 1e-3, max_iterations = 100, return_iterations=True)
    print(f'Tasa de ahorro máxima: {round(root[0],4)}')
    print(f'Pasos en la búsqueda de biseccion: {root[1]}')
