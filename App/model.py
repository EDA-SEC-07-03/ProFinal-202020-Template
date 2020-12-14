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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import shellsort as she
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    try:
        analyzer = {
                    'taxis': None,
                    'connections': None,
                    'components': None,
                    'companias' : None,
                    'paths': None
                    }
        analyzer['companias'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareCompanyName)
        analyzer['taxi'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareTaxiIds)
        analyzer['rango_tiempo'] = m.newMap()        
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def load_taxi(analyzer, server):
    lt.addLast(analyzer['taxi'], server['taxi_id'])
    return analyzer
def load_compañia(analyzer, server):
    if server['company'] == None:
        lt.addLast(analyzer['companias'], 'Independent Owner')
    else:
        lt.addLast(analyzer['companias'], server['company'])
    return analyzer

def addStopConnection(grafo, destination_area, origin_area, service):
    try:
        origin = origin_area
        destination = destination_area
        addStation(grafo, origin)
        peso = service['trip_seconds']
        addStation(grafo, destination)
        addConnection(grafo, origin, destination, peso)
        return grafo
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def agregar_camino(analyser, initial_id, dest_id, server):
    time = int(server['trip_seconds'])
    addStation(analyser, initial_id)
    addStation(analyser, dest_id)
    addConnection(analyser, initial_id, dest_id, time)
    return analyser


def addStation(grafo, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(grafo, stationid):
            gr.insertVertex(grafo, stationid)
        return grafo
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addConnection(grafo, origin, destination, time):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(grafo, origin, destination)
    if edge is None:
        gr.addEdge(grafo, origin, destination, time)
    return grafo
# ==============================
# Funciones de consulta
# ==============================
def getDateTimeTaxiTrip(taxitrip):

    """

    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).

    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'

    Los datos date se pueden comparar con <, >, <=, >=, ==, !=

    Los datos time se pueden comparar con <, >, <=, >=, ==, !=

    """

    tripstartdate = taxitrip['trip_start_timestamp']

    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')

    return taxitripdatetime.date(), taxitripdatetime.time()
def getDateTimeTaxiTrip_end(taxitrip):

    """

    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).

    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'

    Los datos date se pueden comparar con <, >, <=, >=, ==, !=

    Los datos time se pueden comparar con <, >, <=, >=, ==, !=

    """

    tripstartdate = taxitrip['trip_end_timestamp']

    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')

    return taxitripdatetime.date(), taxitripdatetime.time()
# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, initialStation, grafo):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(grafo, initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


# ==============================
# Funciones de Comparacion
# ==============================
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    else:
        return -1
def compareTaxiIds(taxi_1, taxi_2):
    if taxi_1 == taxi_2:
        return 0
    else:
        return 1
def compareCompanyName(compania_1, compania_2):
    if compania_1 == compania_2:
        return 0
    else:
        return 1
def comparador_ascendente(pos1, pos2):
    if int(pos1[1]) > int(pos2[1]):
        return True
    else:
        return False
#===============================
#Funciones requerimiento A
#===============================
def total_taxis(analyzer):
    x = lt.size(analyzer['taxi'])
    return x
def total_companias(analyzer):
    x = lt.size(analyzer['companias'])
    return x
def top_companias_taxis(analyzer, N):
    lst = lt.newList(datastructure= 'ARRAY_LIST',cmpfunction=None)
    dic = analyzer['top_company_taxis']
    dic_to = {}
    x = 0
    for i in range(lt.size(analyzer['companias'])):
        guardar = dic[lt.getElement(analyzer['companias'], i)]
        dic_to[guardar] = lt.getElement(analyzer['companias'], i)
    while x != N:
        maximo = max(dic_to)
        tuplencio = (dic_to[maximo], maximo)
        del dic_to[maximo]
        lt.addLast(lst,tuplencio)
        x +=1
    return lst['elements']
def top_company(analyzer, N):
    lst = lt.newList(datastructure= 'ARRAY_LIST',cmpfunction=None)
    dic = analyzer['top_company']
    dic_to = {}
    x = 0
    for i in range(lt.size(analyzer['companias'])):
        guardar = dic[lt.getElement(analyzer['companias'], i)]
        dic_to[guardar] = lt.getElement(analyzer['companias'], i)
    while x != N:
        maximo = max(dic_to)
        tuplencio = (dic_to[maximo], maximo)
        del dic_to[maximo]
        lt.addLast(lst,tuplencio)
        x +=1
    return lst['elements']
#===============================
#Funciones requerimiento C
#===============================
def ruta_rango_tiempo(analyzer, ida, llegada, rango_tiempo):
    grafos = analyzer['rango_tiempos']
    minimumCostPaths(analyzer, ida, grafos[rango_tiempo])
    camino = minimumCostPath(analyzer, llegada)
    return camino

    
