from clasificador.clasificador import Clasificador
from os import sys, path

def imprimirClasificaciones(clasificaciones):
    """
    Dadas las clasificaciones de las figuras en la imagen, las imprime
    con el siguiente formato:
    [hexadecimal_figura_1] = [clasificacion_figura_1]
    ...
    [hexadecimal_figura_n] = [clasificacion_figura_n]

    Parámetros:
    ----------
    	clasificaciones (dict): contiene las clasificaciones de las figuras, asociándolas
    	con su color RGB en decimal.
    """
    for (color, clasificacion) in clasificaciones.items():
        hex = ("%02x%02x%02x" % color).upper()
        print(hex, "=", clasificacion)

if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("Uso: python3 main.py [ruta_de_imagen]")
    else:
        ruta = sys.argv[1]
        if path.isfile(ruta) and ruta.lower().endswith(".bmp"):
            clasificaciones = Clasificador.clasificarFiguras(ruta)
            imprimirClasificaciones(clasificaciones)
        else:
            print("Ruta introducida no es un archivo bmp válido.")


