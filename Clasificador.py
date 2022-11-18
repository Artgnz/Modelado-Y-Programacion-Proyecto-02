import math

def obtenerDistancias(centros, contornos):
    distancias = {}
    for color in centros:
        lista1 = []
        lista2 = contornos[color]
        for tupla in lista2:
            lista1.append(calcularDistancia(centros[color],lista2[tupla]))
        distancias[color] = lista1
    return distancias

def calcularDistancia(centro, contorno):
    return math.sqrt(((contorno[0]-centro[0])**2) + ((contorno[1]-centro[1])**2))

def
