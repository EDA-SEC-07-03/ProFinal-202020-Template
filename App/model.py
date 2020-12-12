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
        analyzer['companias'] = lt.newList(datastructure='LINKED_LIST', cmpfunction=None)
        analyzer['taxi'] = lt.newList(datastructure='LINKED_LIST', cmpfunction=None)            
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def load_taxi(analyzer, server):
    lt.addFirst(analyzer['taxis'], server['taxi_id'])
    return analyzer
def load_compañia(analyzer, server):
    if server['company'] == None:
        lt.addFirst(analyzer['companias'], 'Independent Owner')
    else:
        lt.addFirst(analyzer['compañias'], server['company'])
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
#===============================
#Funciones rquerimiento A
#===============================
def total_taxis(analyzer):
    x = lt.size(analyzer['taxi'])
    return x
def total_companias(analyzer):
    x = lt.size(analyzer['companias'])
    return x
def top_companias_taxis(analyzer, N):
    x = lt.subList(analyzer['top_company_taxis'],0,N)
    return x
def top_company(analyzer, M):
    x = lt.subList(analyzer['top_company'], 0,M)
    return x