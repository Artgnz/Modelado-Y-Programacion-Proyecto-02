import math
import statistics

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

def suavizarDistancias(distancias):
    distanciasSuavizadas = {}
    for color in distancias:
        lista1 = []
        lista2 = distancias[color]
        for i in lista2:
            lista1.push(statistics.mean(lista1[i-2:i+3]))
        distanciasSuavizadas[color] = lista1
    return distanciasSuavizadas

def obtenerVertices(distancias):
    vertices = {}
    for color in distancias:
        peakIndices = []
        peakIndex = None
        peakValue = None
        signal = distancias[color]
        baseline = statistics.mean(signal)

        for i, value in signal:
            if value > baseline:
                if peakValue == None or value > peakValue:
                    peakValue = value
                    peakIndex = i
                else if value<peakValue and peakValue != None:
                    peakIndices.push(peakIndex)
                    peakIndex = None
                    peakValue = None

        if peakIndex != None:
            peakIndices.push(peakIndex)

        vertices[color] = len(peakIndices)

    return vertices    

def clasificar(vertices):
    clasificacion = {}
    for color in vertices:
        if vertices[color]==3:
            clasificacion[color] = 'T'

        if vertices[color]==4:
            clasificacion[color] = 'C'

        if 5<=vertices[color]<=8:
            clasificacion[color] = 'X'

        if vertices[color]==0 or vertices[color]>8:
            clasificacion[color] = 'O'

    return clasificacion
