from abc import ABC, abstractmethod
import time
import random
import functools
import numpy as np

"""
La idea es que nuestro sensor es el sujeto observable, el que produce los datos, mientras que el sistema es el observador, el que recibe los datos del sensor. 
Solo hay una instancia del Sistema, y además, cuando recibe un nuevo dato, este dato lo pasa a otras clases (chain of responsability) que hagan ya las operaciones.

"""

# -----------------------
# EXCEPCIONES
# -----------------------
class ErrorEnTemperatura(Exception):
    pass

class ErrorEnObservador(Exception):
    pass

class ErrorEnEstrategia(Exception):
    pass

class ErrorEnCadena(Exception):
    pass



# -----------------------
# CLASES
# -----------------------

#PATRÓN DE DISEÑO OBSERVER
class Observable:
    def __init__(self):
        self._observers = []

    def registrar_sistema(self, observer):
        if not isinstance(observer,Observer) :
            print("El sistema debe ser registrado como un observador")
            raise ErrorEnObservador
        self._observers.append(observer)

    def eliminar_sistema(self, observer):
        if observer not in self._observers :
            print("El observador no se encuentra registrado")
            raise ErrorEnObservador
        self._observers.remove(observer)

    def notificar_sistema(self, temperatura):
        for observer in self._observers:
            observer.actualizar(temperatura)

class Observer(ABC):
    @abstractmethod
    def actualizar(self, temperatura):
        pass


class Sensor(Observable): 
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.temperatura = 0

    def establecer_temperatura(self, temperatura):
        if not isinstance(temperatura,list):
            print("La temperatura debe de ir junto a su fecha")
            raise ErrorEnTemperatura
        if len(temperatura) != 2 :
            print("La temperatura debe de ir junto a su fecha")
            raise ErrorEnTemperatura
        if not isinstance(temperatura[1],int) :
            print("La temperatura debe ser un número entero.")
            raise ErrorEnTemperatura
        if not isinstance(temperatura[0],str) :
            print("La fecha de la temperatura debe ser una cadena de texto.")
            raise ErrorEnTemperatura
        self.temperatura = temperatura
        self.notificar_sistema(self.temperatura)



class Sistema(Observer):     #Nuestra sistema recibe los datos del Sensor, y además la clase 'Sistema' sirve como 'Contexto' para aplicar Strategy y elegir la estrategia a llevar a cabo
    #TENEMOS UNA ÚNICA INSTANCIA DE NUESTRO SISTEMA----> SINGLETON
    _unicaInstancia = None

    def __init__(self):
        self._name = "Sistema_temperatura" #Nombre de nuestro sistema
        self._estrategia=None

    @classmethod
    def obtener_instancia(cls) :
        if not cls._unicaInstancia :
            cls._unicaInstancia = cls()
        return cls._unicaInstancia
    
    def actualizar(self, temperatura):  #el error en cuanto al tipo de temperatura ya es tratado en la clase 'Sensor'
        print ("Nueva temperatura - Timestamp: {}, Temperatura: {}".format(temperatura[0],temperatura[1]))
        e = Estadísticos()   #CHAIN OF RESPONSABILITY
        e.establecer_estrategia(self._estrategia)  #Se establece la estrategia a tomar en la clase 'Estadísticos'
        u = UmbralTemperatura(e)
        a = AumentoTemperatura(u)
        t = temperatura[1]
        a.handle_request(t)

    def establecer_estrategia(self,estrategia) :
        if isinstance(estrategia,Estrategia1) or isinstance(estrategia,Estrategia2) or isinstance(estrategia,Estrategia3) :
            self._estrategia = estrategia
        else :
            print("La estrategia debe ser del tipo 1, 2 o 3")
            raise ErrorEnEstrategia
        





#CHAIN OF RESPONSABILITY, donde la temperatura pasa por todas las clases obligatoriamente 
class Manejador(ABC) : 
    def __init__(self,sucesor=None) :
        self.sucesor = sucesor

    def handle_request(self,temperatura) :
        pass





class Estadísticos(Manejador) :    #Esta es nuestra clase para aplicar STRATEGY
    def __init__(self,sucesor=None,estrategia=None,lista_temperaturas_e=[]) :
        if sucesor is not None and not isinstance(sucesor,UmbralTemperatura) and not isinstance(sucesor,AumentoTemperatura) :
            print("Las operaciones a realizar son AumentoTemperatura, UmbralTemperatura y Estadísticos.")
            raise ErrorEnCadena
        super().__init__(sucesor)
        self.estrategia = estrategia
        self.lista_temperaturas_e = lista_temperaturas_e
    def establecer_estrategia(self,estrategia_concreta) : #El error del tipo de estrategia ya es tratado en la clase 'Sistema'
        self.estrategia = estrategia_concreta  
    def handle_request(self,temperatura) :
        self.lista_temperaturas_e.append(temperatura)
        if len(self.lista_temperaturas_e) == 12:
            print(f"Cálculo de estadísticos en base a las temperaturas de los últimos 60 segundos: ")
            self.estrategia.aplicarAlgoritmo(self.lista_temperaturas_e)
            self.lista_temperaturas_e.clear() #se eliminan todos las temperaturas de los últimos 60 segundos una vez se han calculado sus estadísticos

        #Ahora pasamos al siguiente de la cadena:
        if self.sucesor :
            self.sucesor.handle_request(temperatura)


class UmbralTemperatura(Manejador) :
    def __init__(self,sucesor=None,lista_temperaturas_u = []) :
        if sucesor is not None and not isinstance(sucesor,Estadísticos) and not isinstance(sucesor,AumentoTemperatura) :
            print("Las operaciones a realizar son AumentoTemperatura, UmbralTemperatura y Estadísticos.")
            raise ErrorEnCadena
        super().__init__(sucesor)
        self.lista_temperaturas_u = lista_temperaturas_u
    def handle_request(self,temperatura) : #FIJAMOS EL UMBRAL A 27ºC
        self.lista_temperaturas_u.append(temperatura)
        if temperatura > 27 :
            print("Temperatura actual por encima de 27ºC") #SE REALIZA LA OPERACIÓN DE COMPROBAR SI LA TEMPERATURA ACTUAL DEL INVERNADERO ESTÁ POR ENCIMA DEL UMBRAL QUE FIJEMOS
        #Ahora pasamos al siguiente de la cadena:  
        if self.sucesor :
            self.sucesor.handle_request(temperatura)


class AumentoTemperatura(Manejador) :
    def __init__(self,sucesor=None,lista_temperaturas_a = []) :
        if sucesor is not None and not isinstance(sucesor,UmbralTemperatura) and not isinstance(sucesor,Estadísticos) :
            print("Las operaciones a realizar son AumentoTemperatura, UmbralTemperatura y Estadísticos.")
            raise ErrorEnCadena
        super().__init__(sucesor)
        self.lista_temperaturas_a = lista_temperaturas_a
    def handle_request(self,temperatura) :
        self.lista_temperaturas_a.append(temperatura)
        if len(self.lista_temperaturas_a) == 6:
            sol = list(filter(lambda x: x>10,self.lista_temperaturas_a))
            if len(sol) > 0 :
                print("La temperatura ha aumentado más de 10 grados en los últimos 30 segundos.")
            self.lista_temperaturas_a.clear() #una vez han pasado los 30 segundos (hay 6 temperaturas registradas), la lista se establece de nuevo a cero.
        #SE REALIZA LA OPERACIÓN DE comprobar si durante los últimos 30 segundos la temperatura ha aumentado más de 10 grados
        #Ahora pasamos al siguiente de la cadena:
        if self.sucesor :
            self.sucesor.handle_request(temperatura)


#ESTRATEGIAS DE STRATEGY:
class Estrategia(ABC) :
    def aplicarAlgoritmo(self,T) :
        pass


class Estrategia1(Estrategia) :
    def aplicarAlgoritmo(self,T) :
        media = functools.reduce(lambda x,y:x+y,T)/len(T)
        des = np.sqrt(sum(map(lambda x: ((x-media)**2),T))/(len(T)-1))
        print(f"\n\tCálculo de la media y desviación típica: \n\t|\tMedia: {round(media,2)}\n\t|\tDesviación típica: {round(des,2)}\n")
        #CÁLCULO DE LA MEDIA Y DESVIACIÓN TÍPICA CON LA TEMPERATURA


class Estrategia2(Estrategia) :
    def aplicarAlgoritmo(self,T) :
        print("\tCómputo de cuantiles:\n ")
        T = sorted(T)
        cuartil1 = round((T[3]+T[4])/2,0)  #La longitud de T siempre es 12
        cuartil2 = round((T[5]+T[6])/2,0)
        cuartil3 = round((T[9]+T[10])/2,0)
        print(f"\t\tCuartiles: {cuartil1},{cuartil2},{cuartil3}\n") #Calculamos los cuartiles
        #CALCULAMOS LOS CUANTILES DE LA TEMPERATURA


class Estrategia3(Estrategia) :
    def aplicarAlgoritmo(self,T) :
        maximo = lambda a,b: a if (a>b) else b
        minimo = lambda a,b: a if (a<b) else b
        max = functools.reduce(maximo,T)
        min = functools.reduce(minimo,T)
        print(f"\n\tValores máximos y mínimos en un periodo de 60 segundos: máximo:{max}, mínimo:{min}\n")
        #CALCULAMOS LOS VALORES MÁXIMOS Y MÍNIMOS EN UN PERIODO DE 60 SEGUNDOS





if __name__ == "__main__" :
    
    Sistema1 = Sistema.obtener_instancia()
    Sensor1 = Sensor("Temperatura")
    Sensor1.registrar_sistema(Sistema1)
    estrategia1 = Estrategia1()    #instanciamos la estrategia que queramos
    Sistema1.establecer_estrategia(estrategia1)
    cont = 0
    while True :
        #ALGUNOS ERRORES:
        if cont == 1 :
            try :
                t = "NO SOY TEMPERATURA"
                Sensor1.establecer_temperatura(t)
            except Exception as e :
                print("Excepción recibida.")   #INFORMAMOS ÚNICAMENTE DE LAS EXCEPCIONES CAPTURADAS

        elif cont == 3 :
            try :
                estrategia_falsa = "NO SOY ESTRATEGIA"
                Sistema1.establecer_estrategia(estrategia_falsa)
            except Exception as e:
                print("Excepción recibida.")

        elif cont == 5 :
            try :
                s = "NO SOY SISTEMA"
                Sensor1.registrar_sistema(s)
            except Exception as e:
                print("Excepción recibida.")

        elif cont == 7 :
            try:
                Sensor1.eliminar_sistema('NO ESTOY REGISTRADO')
            except Exception as e:
                print("Excepción recibida.")

        #CAMBIOS DE ESTRATEGIA DE MANERA AUTOMÁTICA :
        elif cont == 15 :
            estrategia2 = Estrategia2()
            Sistema1.establecer_estrategia(estrategia2)

        elif cont == 25 :
            estrategia3 = Estrategia3()
            Sistema1.establecer_estrategia(estrategia3)

        t = random.randrange(0, 50)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        temp_nueva = [timestamp, t]
        Sensor1.establecer_temperatura(temp_nueva)
        cont+= 1
        time.sleep(5)






