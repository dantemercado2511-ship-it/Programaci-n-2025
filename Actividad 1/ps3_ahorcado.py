# -*- coding: utf-8 -*-
# Hangman / Ahorcado

# -----------------------------------
# Código de ayuda (helper)
# No necesitas entender cómo funciona internamente,
# pero sí debes saber usar estas funciones (¡lee los docstrings!)
# -----------------------------------

import random



def elegirPalabra(listadoPalabras):
    """
    listadoPalabras (list): lista de palabras (strings)

    Devuelve una palabra elegida al azar del listado.
    
    """
    return random.choice(listadoPalabras)


# -----------------------------------
# Fin del helper
# -----------------------------------


def cargarPalabras():
    """
    Devuelve una lista de palabras válidas. Las palabras son cadenas en minúsculas.

    Dependiendo del tamaño de la lista, esta función puede tardar un poco.
    """
    file = open('palabras.txt', 'r')


    palabras = []

    for palabra in file:
        palabras.append(palabra[:-1])

    file.close()
    return palabras

# Cargamos la lista de palabras en la variable 'listadoPalabras'
# para que esté disponible en todo el programa
# listadoPalabras = cargarPalabras()
# Por default cargarPalabras() deberá seleccionar palabras de longitud 
# mayor e igual a 6, seleccionada del archivo "palabras.txt".



def esPalabraAdivinada(palabraSecreta, letrasMencionadas):
    '''
    palabraSecreta: string, la palabra que el usuario intenta adivinar
    letrasMencionadas: list, letras que ya fueron intentadas
    retorna: booleano, True si todas las letras de palabraSecreta están en letrasMencionadas;
             False en caso contrario
    '''
    for letter in normalizar(palabraSecreta):
        if letter not in letrasMencionadas:
            return False
    return True



def obtenPalabraAdivinada(palabraSecreta, letrasMencionadas):
    '''
    palabraSecreta: string, la palabra que el usuario intenta adivinar
    letrasMencionadas: list, letras que ya fueron intentadas
    retorna: string, con letras y guiones bajos que representan
             el estado parcial de la palabra adivinada hasta ahora.
             Ej.: 'a_ _ le' para 'apple' si solo se adivinó 'a' y 'l' y 'e'.
    '''
    # COMPLETÁ TU CÓDIGO...
    # Sugerencia: construí un string acumulando letra o '_' según corresponda.
    palabra = '    '
    norm = normalizar(palabraSecreta)

    for i in range(len(palabraSecreta)):
        if norm[i] in letrasMencionadas:
            palabra += palabraSecreta[i]
        else:
            palabra += '_'

    return palabra



def obtenLetrasDisponibles(letrasMencionadas):
    '''
    letrasMencionadas: list, letras ya intentadas
    retorna: string, con las letras (a..z) que aún NO se han intentado.
    '''
    # COMPLETÁ TU CÓDIGO ...
    # Sugerencia: empezá del alfabeto 'abcdefghijklmnopqrstuvwxyz' y remové las ya usadas.
    alfabeto = 'abcdefghijklmnñopqrstuvwxyz'

    for letter in letrasMencionadas:
        alfabeto = alfabeto.replace(letter,'')

    return alfabeto

def normalizar(texto):
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ü': 'u',
    }
    for original, simple in reemplazos.items():
        texto = texto.replace(original, simple)
    return texto

def obtenerLetra(letrasMencionadas):
    alfabeto = 'abcdefghijklmnñopqrstuvwxyz'
    while True:
        letra = ''
        letra = input('Ingrese una letra: ')

        if len(letra) != 1:
            print('Debe ingresar solo 1 (UNA) letra\n')
            continue

        if not letra.lower() in alfabeto:
            print('Eso no es una letra!\n')
            continue

        if letra.lower() in letrasMencionadas:
            print('Ya has ingresado esa letra!\n')
            continue
        else:
            return letra.lower()


def ahorcado(palabraSecreta):
    '''
    palabraSecreta: string, la palabra secreta a adivinar.

    Inicia un juego interactivo de Ahorcado.

    * Al inicio, informá cuántas letras tiene palabraSecreta.

    * Pedí al usuario una sola letra por ronda.

    * Informá inmediatamente si su letra aparece o no en la palabra.

    * Tras cada ronda, mostrale el estado parcial de la palabra,
      y también las letras que aún no ha usado.

    Seguí las demás limitaciones descriptas en el enunciado (8 intentos, no
    descontar por letras repetidas, terminar al adivinar toda la palabra o al
    quedarse sin intentos; si pierde, mostrar la palabra).
    '''
    # COMPLETÁ TU CÓDIGO AQUÍ...
    # Sugerencias:
    # - Usá un conjunto/lista para letrasMencionadas
    # - Llevá un contador de intentos restantes (inicialmente 8)
    # - En cada vuelta: mostrar letras disponibles, pedir input, validar que sea 1 letra a-z,
    #   manejar repetidos, actualizar estado, y chequear victoria/derrota.
 

    intentos = 8
    letrasMencionadas = []

    print('¡Bienvenido/a al Ahorcado!')
    print(f'Estoy pensando en una palabra de {len(palabraSecreta)} letras.')

    while True:
        print('\n')
        print(obtenPalabraAdivinada(palabraSecreta, letrasMencionadas), '\n')
        print(obtenLetrasDisponibles(letrasMencionadas), '\n')

        letra = obtenerLetra(letrasMencionadas)
        letrasMencionadas.append(letra)
        if not letra in normalizar(palabraSecreta):
            intentos -= 1

        if intentos == 0:
            print(f'\nTe quedaste sin oportinudades. La palabra secreta era {palabraSecreta}.')
            break

        if esPalabraAdivinada(palabraSecreta, letrasMencionadas):
            print('\n', f'\nMuy bien. La palabra sectreta era: {palabraSecreta}!')
            break


# Cuando termines tu función ahorcado, descomentá estas dos líneas para probar
# (pista: mientras probás, podés elegir vos la palabra secreta)
listadoPalabras = cargarPalabras()
palabraSecreta = elegirPalabra(listadoPalabras)
ahorcado(palabraSecreta)




