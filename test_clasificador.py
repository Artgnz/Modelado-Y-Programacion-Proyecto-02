import unittest
from clasificador import Clasificador
import cv2

class TestClasificador(unittest.TestCase):
    def test__promediarCoordenadas(self):
        """
        Prueba que permite conocer si se pueden promediar las coordenadas correctamente para
        obtener el centro de la figura.
        """
        clasificador = Clasificador()
        sumaCoordenadas = {"(255,255,255)": [1234, 22314], "(0,0,0)": [542, 876]}
        cantidadCoordenadas = {"(255,255,255)": 23, "(0,0,0)": 20}
        promedios = clasificador._Clasificador__promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas)
        esperado = {"(255,255,255)":[54, 970], "(0,0,0)":[27, 44]}
        self.assertEqual(promedios, esperado)


    def test__obtenerDistanciaContornos(self):
        """
        Prueba que permite conocer si las distancias del centro de una figura
        a su contorno se calculan correctamente.
        """
        clasificador = Clasificador()
        path = r'./example_1.bmp'
        im = cv2.imread(path)
        centros = {(78,106,123): [16, 49]}
        distancias = clasificador._Clasificador__obtenerDistanciaContornos(im, centros)
        distancias2 = distancias.get((78,106,123), [])
        distancia = distancias2[0]
        esperado = 11.0
        self.assertEqual(distancia, esperado)
        
if __name__ == "__main__":
    unittest.main()
