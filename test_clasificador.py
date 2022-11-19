import unittest
from clasificador import Clasificador

class TestClasificador(unittest.TestCase):
    def test__promediarCoordenadas(self):
        "Prueba que pueda promediar coordenadas satisfactoriamente."
        clasificador = Clasificador()
        sumaCoordenadas = {"(255,255,255)": [1234, 22314], "(0,0,0)": [542, 876]}
        cantidadCoordenadas = {"(255,255,255)": 23, "(0,0,0)": 20}
        promedios = clasificador._Clasificador__promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas)
        esperado = {"(255,255,255)":[54, 970], "(0,0,0)":[27, 44]}
        self.assertEqual(promedios, esperado)
        
if __name__ == "__main__":
    unittest.main()
