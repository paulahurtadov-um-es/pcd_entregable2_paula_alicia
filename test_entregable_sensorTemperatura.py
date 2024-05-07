import Entrega_PRAC2 as e

import pytest

@pytest.fixture  #añadimos el decorador
#Creamos las instancias que necesitamos para nuestras pruebas
def sistema():
    return e.Sistema.obtener_instancia()


@pytest.fixture
def sensor() :
    return e.Sensor("Temperatura")




def test_registrar_sistema(sensor) :
    with pytest.raises(e.ErrorEnObservador):
        sensor.registrar_sistema('NO SOY SISTEMA')



def test_eliminar_sistema(sensor) :
    with pytest.raises(e.ErrorEnObservador):
        sensor.eliminar_sistema('NO SOY SISTEMA')



def test_registrar_sistema_correctamente(sensor,sistema) :
     sensor.registrar_sistema(sistema)
     sensor.establecer_temperatura(['2024-05-06 20:49:29',35])
     assert sistema in sensor._observers



def test_temperatura_error_1(sensor) :
    with pytest.raises(e.ErrorEnTemperatura):
        sensor.establecer_temperatura(1)



def test_temperatura_error_2(sensor) :
    with pytest.raises(e.ErrorEnTemperatura):
        sensor.establecer_temperatura([1234,1234])



def test_temperatura_error_3(sensor):
    with pytest.raises(e.ErrorEnTemperatura):
            sensor.establecer_temperatura(['2024-05-06 20:49:29',"0"])


def test_temperatura_correcta(sensor,sistema) :
    t = ['2024-05-06 20:49:29',35]
    estrategia1 = e.Estrategia1()
    sistema.establecer_estrategia(estrategia1)
    sensor.establecer_temperatura(t)
    assert sensor.temperatura == t


def test_establecer_estrategia(sistema) :
    with pytest.raises(e.ErrorEnEstrategia):
            sistema.establecer_estrategia("NO SOY ESTRATEGIA")



def test_establecer_estrategia_correctamente(sensor,sistema) :
    estrategia1 = e.Estrategia1()
    sistema.establecer_estrategia(estrategia1)
    sensor.establecer_temperatura(['2024-05-06 20:49:29',35])
    assert sistema._estrategia == estrategia1


"""
Podemos observar que al ejecutar pytest en nuestro terminal, todos los test pasan las pruebas con éxito.

"""


