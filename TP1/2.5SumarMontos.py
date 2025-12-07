user_input = ''
monto = 0

while True:
    user_input = input('Ingrese un numero(Enter para continuar): ')
    if user_input == '':
        break
    try:
        monto += float(user_input)
    except:
        print('Debe ingresar un numero')

print(f'El monto total es: {monto}')
