from math import sqrt
from statistics import mean

class Clasificador:

    @staticmethod
    def obtenerDistancias(centros, contornos):
        distancias = {}
        for color in centros:
            distanciasColor = []
            listaContornos = contornos[color]
            for tupla in listaContornos:
                distanciasColor.append(calcularDistancia(centros[color],listaContornos[tupla]))
            distancias[color] = distanciasColor
        return distancias

    @staticmethod
    def calcularDistancia(centro, contorno):
        return math.sqrt(((contorno[0]-centro[0])**2) + ((contorno[1]-centro[1])**2))

    @staticmethod
    def suavizarDistancias(distancias):
        distanciasSuavizadas = {}
        for color in distancias:
            distanciasSuavizadasColor = []
            listaDistancias = distancias[color]
            for i in listaDistancias:
                distanciasSuavizadasColor.push(statistics.mean(listaDistancias[i-2:i+3]))
                distanciasSuavizadas[color] = distanciasSuavizadasColor
        return distanciasSuavizadas

    @staticmethod
    def obtenerVertices(distancias):
        vertices = {}
        for color in distancias:
            indicesCresta = []
            indiceCresta = None
            valorCresta = None
            listaDistancias = distancias[color]
            promedio = statistics.mean(listaDistancias)
            for i, valor in listaDistancias:
                if valor > promedio:
                    if valorCresta == None or valor > valorCresta:
                        valorCresta = valor
                        indiceCresta = i
                    elif valor < valorCresta and valorCresta != None:
                        indicesCresta.push(indiceCresta)
                        indiceCresta = None
                        valorCresta = None
            if indiceCresta != None:
                indicesCresta.push(indiceCresta)
            vertices[color] = len(indicesCresta)
        return vertices    

    @staticmethod
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
