import cv2
import math
from statistics import mean

class Clasificador:

    @staticmethod
    def __suavizarDistancias(distancias):
        distanciasSuavizadas = {}
        tamanoVentana = 2
        for color in distancias:
            distanciasSuavizadasColor = []
            distanciasColor = distancias[color]
            distanciasExpandidas = distanciasColor[-tamanoVentana:] + distanciasColor + distanciasColor[0:tamanoVentana]
            for i in range(tamanoVentana, len(distanciasColor) + tamanoVentana):
                ventana = distanciasExpandidas[i - tamanoVentana : i + tamanoVentana + 1]
                promedio = mean(ventana)
                distanciasSuavizadasColor.append(round(promedio,2))
            distanciasSuavizadas[color] = distanciasSuavizadasColor
        return distanciasSuavizadas

    @staticmethod
    def __obtenerVertices(distancias):
        vertices = {}
        for color in distancias:
            indicesCresta = []
            indiceCresta = None
            valorCresta = None
            listaDistancias = distancias[color]
            promedio = mean(listaDistancias)
            i = 0
            for valor in listaDistancias:
                if valor > promedio:
                    if valorCresta == None or valor > valorCresta:
                        indiceCresta = i
                        valorCresta = valor
                elif valor < promedio and valorCresta != None:
                    indicesCresta.append(indiceCresta)
                    indiceCresta = None
                    valorCresta = None
                    i += 1
            if indiceCresta != None:
                indicesCresta.append(indiceCresta)
            vertices[color] = len(indicesCresta)
        return vertices

    @staticmethod
    def __clasificar(vertices):
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

    def __obtenerCentros(imagen):
        sumaCoordenadas = {}
        cantidadCoordenadas = {}
        colorFondo = imagen[0][0]
        for fila in range(len(imagen)):
            for col in range(len(imagen[fila])):
                color = tuple(imagen[fila][col])
                if (color != colorFondo).any():
                    viejaSuma = sumaCoordenadas.get(color, [0,0])
                    sumaCoordenadas[color] = [viejaSuma[0] + col, viejaSuma[1] + fila]
                    cantidadCoordenadas[color] = cantidadCoordenadas.get(color, 0) + 1
        return Clasificador.__promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas)

    @staticmethod
    def __promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas):
        promedios = {}
        for (color, coordenadas) in sumaCoordenadas.items():
            promedioX = round(coordenadas[0] / cantidadCoordenadas[color])
            promedioY = round(coordenadas[1] / cantidadCoordenadas[color])
            promedios[color] = [promedioX, promedioY]
        return promedios

    @staticmethod
    def __obtenerDistanciaContornos(im, centros):
        """
        Regresa un diccionario que contiene las distancias desde el centro de cada figura
        hasta cada punto de su contorno

        Parámetros
        ----------
            im: bitmap
                la imagen en la cual se buscan los contornos
            centros: diccionario
                contiene las coordenadas de los centros de cada figura
        
        Returns
        -------
            distancias: diccionario
                contiene las distancias desde el centro de cada figura
                hasta cada punto de su contorno
        """
        distancias = {}
        for (r,g,b) in centros:
            centro = centros.get((r,g,b), [])
            distancias[(r,g,b)] = Clasificador.__dda(im, centro)
        return distancias

    @staticmethod
    def __dda(im, centro):
        """
        Dado el centro de una figura calcula la distancia hasta cada uno de sus pixeles que conforman su contorno

        Parámetros
        ----------
            im: bitmap
                la imagen en la cual se encuentra la figura
            centro: lista
                contiene las coordenadas del centro de la figura
        
        Returns
        -------
            distancias: lista
                contiene las distancias desde cada uno de los pixeles del contorno hasta el centro de la figura
        """
        x = centro[0]
        y = centro[1]
        angulo = 0

        h = 20
        distancias = []
        while(angulo < 2*math.pi):
            xf = x + (h * math.cos(angulo))
            yf = y + (h * math.sin(angulo))
            
            dx = xf - x
            dy = yf - y
            
            pasos = max(abs(dx), abs(dy))
            llegue = False
            xa = x
            ya = y
            while(llegue == False):
                xa = xa + (dx/pasos)
                ya = ya + (dy/pasos)
                # Fórmula de distancia entre dos puntos.
                distancia = math.sqrt(((xa-x)**2) + ((ya-y)**2))
                if (ya < 0) | (ya > len(im)-1) | (xa < 0) | (xa > len(im[0])-1):
                    llegue = True
                    angulo = angulo + math.pi/360
                    distancias.append(distancia)

                elif ((im[round(ya)][round(xa)] != im[round(y)][round(x)]).any()):
                    llegue = True
                    angulo = angulo + math.pi/360
                    distancias.append(distancia)
        return distancias
