import cv2
import math
class Clasificador:

    @staticmethod
    def obtenerDistanciaContornos(im, centros):
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
        h = 10
        distancias = []
        while(angulo < 2*math.pi):
            xf = x + (h * math.cos(angulo))
            yf = y + (h * math.sin(angulo))
        
            dx = xf - x
            dy = yf - y
            
            pasos = max(abs(dx), abs(dy))
            distancia = 0
            llegue = False
            xa = x
            ya = y
            while(llegue == False):
                xa = xa + (dy/pasos)
                ya = ya + (dx/pasos)
                distancia = distancia + 1

                if (xa < 0) | (xa > len(im)) | (ya < 0) | (ya > len(im[0])):
                    llegue = True
                    angulo = angulo + math.pi/360
                    distancias.append(distancia)

                elif((im[round(xa)][round(ya)] != im[x][y]).any()):
                    llegue = True
                    angulo = angulo + math.pi/360
                    distancias.append(distancia)
            
        return distancias
