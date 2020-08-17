"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
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
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

import config as cf
import sys
import csv
from Sorting import mergesort as srt
from DataStructures import listiterator as it
from ADT import list as slt
from time import process_time 

def loadCSVFile (file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lst.append(row)
    except:
        del lst[:]
        print("Se presento un error en la carga del archivo")
    
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos de Películas")
    print("2- Cargar Datos de Casting")
    print("3- Encontrar películas buenas")
    print("4- Crear ranking películas")
    print("5- Contar los elementos de la Lista")
    print("6- Contar elementos filtrados por palabra clave")
    print("7- Consultar elementos a partir de dos listas")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        for element in lst:
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return counter

def countElementsByCriteria(criteria, column, lst):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    return 0

def searchGoodMovies(movies,casting):
    dictretorno={}
    for x in range(len(movies)):
        if float(movies[x]["vote_average"])>=6:
            director=casting[x]["director_name"]
            if director in dictretorno:
                dictretorno[director][0]+=1
                dictretorno[director][1]+=float(movies[x]["vote_average"])
            else:
                dictretorno[director]=[1,0]
                dictretorno[director][1]=float(movies[x]["vote_average"])
    return dictretorno
def ordenarAverageAsc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_average'])>float(mov2['vote_average']):
        return True
    return False
def ordenarAverageDesc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_average'])<float(mov2['vote_average']):
        return True
    return False
def ordenarCountAsc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_count'])>float(mov2['vote_count']):
        return True
    return False
def ordenarCountDesc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_count'])<float(mov2['vote_count']):
        return True
    return False

def createRankingMovies(listamovies:list,movies:int,orden:bool,countoaverage:bool)->list:
    listaretorno=[]
    listmovies=slt.newList('SINGLE_LINKED')
    if countoaverage:#Count=True Average=False B)
        if orden:#Asc=True, Desc=False B)
            srt.mergesort(listmovies,ordenarCountAsc)
        else:
            srt.mergesort(listmovies,ordenarCountDesc)
    else:
        if orden:
            srt.mergesort(listmovies,ordenarAverageAsc)
        else:
            srt.mergesort(listmovies,ordenarAverageDesc)
    listaretorno.append(slt.lastElement(listmovies))
    return listaretorno
def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el arivo
    Args: None
    Return: None 
    """
    listamovies = [] #instanciar una lista vacia
    listacasting = []
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                loadCSVFile("Data/SmallMoviesDetailsCleaned.csv", listamovies) #llamar funcion cargar datos
                print("Datos cargados, "+str(len(listamovies))+" elementos cargados")
                print(type(listamovies))
            elif int(inputs[0])==2:
                loadCSVFile("Data/MoviesCastingRaw-small.csv",listacasting)
                print("Datos cargados, "+str(len(listacasting))+" elementos cargados")
                print(type(listacasting))
            elif int(inputs[0])==3:
                goodmovies=searchGoodMovies(listamovies,listacasting)
                for each in goodmovies:
                    print("Director: "+each)
                    print("Películas buenas: "+str(goodmovies[each][0]))
                    print("Votos Promedio: "+str(round(goodmovies[each][1]/goodmovies[each][0],2)))
            elif int(inputs[0])==4:
                quantity=int(input("Escriba el tamaño del ranking que desea crear (Mayor o igual a 10): "))
                while quantity<10:
                    print("La cantidad debe ser mayor de 10")
                    quantity=int(input("Escriba el tamaño del ranking que desea crear: "))
                avgorcount=input("Escriba Average o Count según lo que desee: ").lower()
                ascordesc=input("Escriba Asc para orden ascendente, o Desc para orden descendente: ").lower()
                if avgorcount=="count":
                    if ascordesc=="asc":
                        ranking=createRankingMovies(listamovies,quantity,True,True)
                    else:
                        ranking=createRankingMovies(listamovies,quantity,False,True)
                else:
                    if ascordesc=="asc":
                        ranking=createRankingMovies(listamovies,quantity,True,False)
                    else:
                        ranking=createRankingMovies(listamovies,quantity,False,False)
                for each in ranking:
                    print("llave")
                    print(each)
                    print("clave")
                    print(ranking[each])
                    break
            elif int(inputs[0])==5: #opcion 2
                if len(lista)==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene "+str(len(lista))+" elementos")
            elif int(inputs[0])==6: #opcion 3
                criteria =input('Ingrese el criterio de búsqueda\n')
                counter=countElementsFilteredByColumn(criteria, "nombre", lista) #filtrar una columna por criterio  
                print("Coinciden ",counter," elementos con el crtierio: ", criteria  )
            elif int(inputs[0])==7: #opcion 4
                criteria =input('Ingrese el criterio de búsqueda\n')
                counter=countElementsByCriteria(criteria,0,lista)
                print("Coinciden ",counter," elementos con el crtierio: '", criteria ,"' (en construcción ...)")
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
if __name__ == "__main__":
    main()
