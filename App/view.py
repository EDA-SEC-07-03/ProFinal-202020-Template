"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________
doc_1 =  'taxi-trips-wrvz-psew-subset-small.csv'
doc_2 = 'taxi-trips-wrvz-psew-subset-medium.csv'
doc_3 = 'taxi-trips-wrvz-psew-subset-large.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Elegir archivo y cargar informacion")
    print("3- Total de taxis")
    print("4- Total de Compañias")
    print("5- Top compañias taxis afiliados")
    print("6- top compañias por servicios")
    print('7- mejor camino entre zonas y rango horario')
    print("0-salir")
"""
Menu principal
"""
def menu_principal():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = controller.init()
        elif int(inputs[0]) == 2:
            print("\nCargando información de bicicletas ....")
            eleccion = int(input("Escriba 1 para el archivo pequeño, 2 para el mediano y tres para el grande: "))
            if eleccion == 1:
                servicefile = doc_1
            if eleccion == 2:
                servicefile = doc_2
            if eleccion == 3:
                servicefile = doc_3
            controller.loadServices_reqA(cont, servicefile)
        elif int(inputs[0]) == 3:
            print("El total de taxis fue: ")
            print(controller.cantidad_taxis(cont))
        elif int(inputs[0]) == 4:
            print("El total de compañias fue: ")
            print(controller.cantidad_companias(cont))
        elif int(inputs[0]) == 5:
            y = int(input("De que tamaño quiere el top de compañias por taxis afiliados: "))
            print('Este es el top ordenado de mayor a menor')
            print(controller.top_c_taxis(cont, y))
        elif int(inputs[0]) == 6:
            x = int(input("De que tamaño quiere el top de compañias por servicios: "))
            print('Este es el top ordenado de mayor a menor')
            print(controller.top_companias(cont, x))
        elif int(inputs[0]) == 7:
            z = int(input("Digite el codigo del lugar de salida: "))
            llegada = int(input("Digite el codigo del lugar de llegada: "))
            tiempo_1 = input("ponga el limite inferior del rango horario en formato (h:min:seg): ")
            tiempo_2 = input("ponga el limite superior del rango de horario en formato (h:min:seg): ")
            print(controller.camino_menor(cont, z, llegada, tiempo_1, tiempo_2))
        else:
            sys.exit(0)
menu_principal()