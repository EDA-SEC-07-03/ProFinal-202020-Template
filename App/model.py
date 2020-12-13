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

def addStopConnection(analyzer, lastservice, servicess, service):
    try:
        origin = servicess
        destination = lastservice
        addStation(analyzer, origin)
        peso = str(service['tripduration'])
        addStation(analyzer, destination)
        addConnection(analyzer, origin, destination, time)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def agregar_camino(analyser, initial_id, dest_id, server):
    time = int(server['tripduration'])
    addStation(analyser, initial_id)
    addStation(analyser, dest_id)
    addConnection(analyser, initial_id, dest_id, time)
    return analyser


def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stationid):
            gr.insertVertex(analyzer['connections'], stationid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addConnection(analyzer, origin, destination, time):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, time)
    return analyzer
# ==============================
# Funciones de consulta
# ==============================

# ==============================
# Funciones Helper
# ==============================

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
    elif (stop > stopcode):
        return 1
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