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
        if lt.isPresent(analyzer['taxi'], server['taxi_id']) == 0:
            model.load_taxi(analyzer, server)
        if lt.isPresent(analyzer['companias']) == 0:
            model.load_compañia(analyzer, server)
            dic_company_taxis[server['company']] = 1
            dic_quantity[server['company']] = 1
        if (lt.isPresent(analyzer['taxi'], server['taxi_id']) == 0) and (lt.isPresent(analyzer['companias']) != 0):
            dic_company_taxis[server['company']] += 1
        else:
            dic_quantity[server['company']] += 1
    analyzer['top_company_taxis'] = max_company(dic_company_taxis)
    analyzer['top_company'] = max_company(dic_quantity)
    return analyzer
    

def max_company(dic):
    lst = lt.newList()
    for i in dic:
        x = max(dic)
        y = dic[x]
        lt.addLast(lst, (x,y))
        dic[x] = 0
    return lst
        

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________