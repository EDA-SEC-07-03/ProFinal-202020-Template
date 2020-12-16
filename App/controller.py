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

import config as cf
from App import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error
import datetime
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():

    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadServices_reqA(analyzer, serverfile):
    serverfile = cf.data_dir + serverfile
    input_file = csv.DictReader(open(serverfile, encoding="utf-8"),
                                delimiter=",")
    dic_company_taxis = {}
    dic_quantity = {}
    for server in input_file:
        if (server['taxi_id'] != None) and (server['company']) != None:
            if lt.isPresent(analyzer['taxi'], server['taxi_id']) == 0:
                model.load_taxi(analyzer, server)
                if lt.isPresent(analyzer['companias'],server['company']) == 0:
                    model.load_compañia(analyzer, server)
                    dic_company_taxis[server['company']] = 1
                    dic_quantity[server['company']] = 1
                if (lt.isPresent(analyzer['companias'], server['company']) != 0):
                    dic_company_taxis[server['company']] += 1
            else:
                dic_quantity[server['company']] += 1
        if (server['pickup_community_area'] != None) and (server['pickup_community_area'] != '') and (server['dropoff_community_area'] != '') and (server['dropoff_community_area'] != None):
            load_services_req_C(analyzer, server)
    analyzer['top_company_taxis'] = dic_company_taxis
    analyzer['top_company'] = dic_quantity
    return analyzer

def load_services_req_C(analyzer,server):
    dia_hora_inicio = model.getDateTimeTaxiTrip(server)[1]
    dia_hora_fin = model.getDateTimeTaxiTrip_end(server)[1]
    rango_tiempo = (dia_hora_inicio, dia_hora_fin)
    mapa = analyzer['rango_tiempo']
    nombre_grafo = analyzer['connections']
    rango_conectados = {}
    grafos = {}
    conectados = m.newMap(comparefunction=comparador_ejemplo)
    inicio = server['pickup_community_area']
    llegada = server['dropoff_community_area']
    tuplencio = (inicio, llegada)
    if m.contains(mapa,rango_tiempo) == False:
        m.put(mapa,rango_tiempo, 1)
        grafos[rango_tiempo] =  nombre_grafo
        grafo = grafos[rango_tiempo] 
        model.addStopConnection(grafo, llegada,inicio,server)
        rango_conectados[rango_tiempo] = conectados
        ubicacion = rango_conectados[rango_tiempo]
        m.put(ubicacion, tuplencio, server['trip_seconds'])
    grafo = grafos[rango_tiempo]
    ubicacion = rango_conectados[rango_tiempo]
    try:
        if m.contains(ubicacion, tuplencio) is not True:
            model.addStopConnection(grafo,llegada, inicio, server)
            m.put(ubicacion, tuplencio, server['trip_seconds'])
        analyzer['rango_tiempos'] =  grafos
        return analyzer
    except Exception as exp:
        error.reraise(exp, print(rango_conectados[rango_tiempo]))


    
def comparador_ejemplo(key_1, key_2):
    if key_1 == key_2:
        return 1
    else: 
        return 0      
def transformador_hora(hora):
    hora=datetime.datetime.strptime(hora,"%H:%M:%S")
    hora=hora.time()
    return hora

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def cantidad_taxis(analyzer):
    x = model.total_taxis(analyzer)
    return x
def cantidad_companias(analyzer):
    x = model.total_companias(analyzer)
    return x
def top_c_taxis(analyzer, N):
    x = model.top_companias_taxis(analyzer, N)
    return x
def top_companias(analyzer, M):
    x = model.top_company(analyzer, M)
    return x
def camino_menor(analyzer, ida, llegada, tiempo_1, tiempo_2):
    rango_tiempo = transformador_hora(tiempo_1)
    rango_t = transformador_hora(tiempo_2)
    x = model.ruta_rango_tiempo(analyzer, ida, llegada, rango_tiempo, rango_t)
    return x 