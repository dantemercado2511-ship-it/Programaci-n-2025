salario_anual = float(input('Introduzca su salario anual: '))
parte_ahorrada = float(input('Introduzca el porcentaje de su salario para ahorrar, como decimal: '))
osto_total = float(input('Introduzca el coste de la casa de sus sueños: '))
parte_pago_inicial = 0.25
ahorro_actual = 0.0
r = 0.04
salario_mensual = salario_anual / 12

meses = 0
while True:
    ahorro_actual *= 1 + r/12
    ahorro_actual += salario_mensual * parte_ahorrada
    meses += 1
    if ahorro_actual >= costo_total * parte_pago_inicial:
        break

print(f'Numero de meses: {meses}')

