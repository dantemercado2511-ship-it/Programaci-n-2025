import ast
import os
import sys

def extraer_fuente(texto, nodo):
    """Extrae el código fuente exacto de un nodo usando offsets."""
    lineas = texto.splitlines(True)
    start = nodo.lineno - 1
    end = nodo.end_lineno
    return "".join(lineas[start:end])

def dividir_modulo(path_modulo):
    nombre_archivo = os.path.basename(path_modulo)
    nombre_modulo, _ = os.path.splitext(nombre_archivo)

    # Carpeta raíz con el nombre del módulo
    carpeta_salida = nombre_modulo
    carpeta_classes = os.path.join(carpeta_salida, "class")
    carpeta_functions = os.path.join(carpeta_salida, "function")

    os.makedirs(carpeta_classes, exist_ok=True)
    os.makedirs(carpeta_functions, exist_ok=True)

    with open(path_modulo, "r", encoding="utf8") as f:
        codigo = f.read()

    tree = ast.parse(codigo)

    for nodo in tree.body:
        # Función suelta
        if isinstance(nodo, ast.FunctionDef):
            nombre = nodo.name
            fuente = extraer_fuente(codigo, nodo)

            destino = os.path.join(carpeta_functions, f"{nombre}.txt")
            with open(destino, "w", encoding="utf8") as f:
                f.write(fuente)

            print(f"✔ función {nombre} → {destino}")

        # Clase
        elif isinstance(nodo, ast.ClassDef):
            nombre_clase = nodo.name

            carpeta_clase = os.path.join(carpeta_classes, nombre_clase)
            os.makedirs(carpeta_clase, exist_ok=True)

            # Archivo con la clase entera
            fuente_clase = extraer_fuente(codigo, nodo)
            archivo_clase = os.path.join(carpeta_clase, f"{nombre_clase}.txt")

            with open(archivo_clase, "w", encoding="utf8") as f:
                f.write(fuente_clase)

            print(f"✔ clase {nombre_clase} → {archivo_clase}")

            # Métodos dentro de la clase
            for sub in nodo.body:
                if isinstance(sub, ast.FunctionDef):
                    nombre_metodo = sub.name
                    fuente_metodo = extraer_fuente(codigo, sub)

                    archivo_metodo = os.path.join(
                        carpeta_clase,
                        f"{nombre_clase}.{nombre_metodo}.txt"
                    )

                    with open(archivo_metodo, "w", encoding="utf8") as f:
                        f.write(fuente_metodo)

                    print(f"    ↳ método {nombre_clase}.{nombre_metodo} → {archivo_metodo}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python dividir_modulo.py archivo.py")
        sys.exit(1)

    dividir_modulo(sys.argv[1])

