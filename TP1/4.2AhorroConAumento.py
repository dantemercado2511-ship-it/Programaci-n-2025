salario_anual = float(input('Introduzca su salario anual: '))
parte_ahorrada = float(input('Introduzca el porcentaje de su salario para ahorrar, como decimal: '))
costo_total = float(input('Introduzca el coste de la casa de sus sueños: '))
aumento_semi_anual = float(input('Introduzca el aumento semestral, en decimales: '))
parte_pago_inicial = 0.25
ahorro_actual = 0.0
r = 0.04
salario_mensual = salario_anual / 12

meses = 0
while True:
    ahorro_actual *= 1 + r/12
    ahorro_actual += salario_mensual * parte_ahorrada
    meses += 1
    if meses % 6 == 0:
        salario_mensual *= 1 + aumento_semi_anual
    if ahorro_actual >= costo_total * parte_pago_inicial:
        break
    print(f'ahorro en el mes {meses}: {ahorro_actual}')

print(f'ahorro: {ahorro_actual}')
print(f'Numero de meses: {meses}')

