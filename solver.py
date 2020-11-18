#!/usr/bin/python3

import sys
from fractions import Fraction
from decimal import Decimal
import copy
from itertools import combinations
from itertools import permutations 

# Datos generales del solver
salida = None # Archivo de salida 
matriz = [] # Guarda los números
id_problema = 1 # Determina el tipo de problema (mochila o alineamiento de secuencias)
algoritmo = 1 # Determinar si se resuelve por algoritmo de fuerza bruta o programación dinámica
nom_archivo = "" # Nombre de archivo de salida

# Variables para el problema de secuencias
secuencia1 = ""
secuencia2 = ""
scorefinal = 0
resultados = []

# Variables para el problema de mochila

###########################################################################################################
#----------------------------------------------------------------------------------------------------------
#   Clase Fracción y métodos
#   Se usó de referencia la clase "Fraction" implementada por msarialp en https://gist.github.com/mustaa/2350807
#----------------------------------------------------------------------------------------------------------
##########################################################################################################
def gcd(num, denom):
#Función que retorna el máximo común divisor
    if (num == 0 or denom == 0):
        return 1
    
    while num != denom:
        if num > denom:
            num = num - denom
        else:
            denom = denom - num
    return num

class Fraccion:
#Clase Fracción
    def __init__(self, num, denom):
        # Constructor, recibe el numerador y denominador, para luego simplificar la fracción
        self.simplificar(num, denom)
        
    def simplificar(self, num, denom):
        # Función que simplifica la fracción usando el máximo común divisor. Asigna los nuevos valores al numerador y denominador
        self.num = int(num / gcd(abs(num), abs(denom)))
        self.denom = int(denom / gcd(abs(num), abs(denom)))
        if self.denom < 0:
            self.denom = abs(self.denom)
            self.num = -1*self.num
        elif self.denom == 0:
            raise ZeroDivisionError
        elif self.num == 0:
            self.denom = 1
            
    def simplificar_nomod(self, num, denom):
        # Función que simplifica la fracción (sin modificar al asignar) usando el máximo común divisor.
        #Retorna los nuevos valores al numerador y denominador en una tupla
        num1 = int(num / gcd(abs(num), abs(denom))) # Simplificar numerador y denominador
        denom1 = int(denom / gcd(abs(num), abs(denom)))
        if denom1 < 0: # Posibles cambios de signo de numerador y denominador
            denom1 = abs(denom1)
            num1 = -1*num1
        elif denom1 == 0: # Se indefine la fracción
            raise ZeroDivisionError
        elif num1 == 0:
            denom1 = 1
        return num1, denom1 # Retornar tupla
        
    def sum(self, other):
        # Función que suma 2 fracciones. Actualiza el resultado en la fracción izquierda 
        num = self.num*other.denom + self.denom*other.num
        denom = self.denom*other.denom
        self.simplificar(num, denom)
    
    def sub(self, other):
        # Función que resta 2 fracciones. Actualiza el resultado en la fracción izquierda
        num = self.num*other.denom - self.denom*other.num
        denom = self.denom*other.denom
        self.simplificar(num, denom)

    def sub_nomod(self, other):
        # Función que resta 2 fracciones. No realiza modificaciones a la fracción izquierda. Retorna una tupla [numerador,denominador] simplificados
        num = self.num*other.denom - self.denom*other.num # Guardar resultado de la resta
        denom = self.denom*other.denom
        return self.simplificar_nomod(num, denom) # Retornar tupla
    
    def mul(self, other):
        # Función que multiplica 2 fracciones. Actualiza el resultado en la fracción izquierda
        num = self.num*other.num
        denom = self.denom*other.denom
        self.simplificar(num, denom)
    
    def div(self, other):
        # Función que divide 2 fracciones. Actualiza el resultado en la fracción izquierda
        num = self.num*other.denom
        denom = self.denom*other.num
        self.simplificar(num, denom)

    def div_nomod(self, other):
        # Función que divide 2 fracciones. No realiza modificaciones a la fracción izquierda. Retorna una tupla [numerador,denominador] simplificados
        num = self.num*other.denom # Guardar resultado de la división
        denom = self.denom*other.num
        return self.simplificar_nomod(num, denom) # Retornar tupla

    def comparar(self, other):
        # Función que compara 2 fracciones para determinar cuál es mayor.
        #No realiza modificaciones. Retorna True si la fracción de la derecha es mayor, y False en caso contrario
        tupla = self.sub_nomod(other)
        numero = tupla[0]
        if (numero >= 0):
            return False
        return True

    def get_num(self):
        #Función que retorna el numerador de la fracción
        return self.num

    def get_denom(self):
        #Función que retorna el denominador de la fracción
        return self.denom    

    def __str__(self):
        # Función que retorna la fracción como un string 
        if self.denom == 1 or self.num == 0:
            return str(self.num)
        else:
            return '%s/%s' %(self.num, self.denom)

###########################################################################################################
#----------------------------------------------------------------------------------------------------------
#Manual del programa (-h)
#----------------------------------------------------------------------------------------------------------
###########################################################################################################

def manual():
    print("\n")    
    print("##########################################################################################################")
    print("----------------------------------------------------------------------------------------------------------")
    print("Inicio Sección Ayuda")
    print("----------------------------------------------------------------------------------------------------------")
    print("##########################################################################################################")
    print("\nEstudiante-> Ricardo Víquez Mora\n")
    print("----------------------------------------------------------------------------------------------------------")
    print("\nDESCRIPCIÓN DEL PROGRAMA:")
    print("Este programa es una implementación del método simplex para resolver problemas de minimización y maximización")
    print("en programación lineal.\n")
    print("----------------------------------------------------------------------------------------------------------")
    print("\nCÓMO USAR EL PROGRAMA:")
    print("- Si no se ha hecho, colocar este archivo en el mismo directorio que los archivos de los problemas a")
    print("resolver en formato (.txt)")
    print("- Ejecutar terminal dentro del mismo directorio")
    print("- En la terminal, escribir los parámetros correspondientes de línea de comandos (ver sección 'PARÁMETROS DE LÍNEA DE COMANDOS')")
    print("- Presionar la tecla ENTER para ejecutar el programa")
    print("\nNota: La solución, con los pasos intermedios se guarda automáticamente en un archivo .txt siguiendo el siguiente formato:")
    print("\n    nombre_archivo_entrada + _solution.txt\n")
    print("Donde:")
    print("- 'nombre_archivo_entrada' es el nombre del archivo de entrada.")
    print("- '_solution.txt' es el sufijo agregado al archivo de salida\n")
    print("----------------------------------------------------------------------------------------------------------")
    print("\nPARÁMETROS DE LÍNEA DE COMANDOS:")   
    print("\n    python simplex.py [-h] archivo.txt\n")     
    print("Donde:")
    print("- El parámetro 'simplex.py' es el nombre del archivo ejecutable.")
    print("- El parámetro '-h' es opcional, y muestra una descripción de como usar el programa, parámetros y formato de")
    print("archivo de entrada.")
    print("- El parámetro 'archivo.txt' es el nombre del archivo de entrada (No se debe de incluir la extensión (.txt)")
    print("en este parámetro).")
    print("\n\nFORMATO DE ARCHIVO DE ENTRADA:")
    print("La estructura del archivo de entrada consiste en elementos separados por coma y en diferentes líneas/filas")
    print("de la siguiente forma:")
    print("\n    método, optimización, Número de variables de decisión, Número de restricciones\n")
    print("\n    coeficientes de la función objetivo\n")
    print("\n    coeficientes de la restricción, signo de restricción, número en la derecha de la restricción\n")
    print("Donde:")
    print("- 'método' es un entero [ 0=Simplex, 1=GranM, 2=DosFases], que es el método para resolver el problema")    
    print("- 'optimización' se indica con min o max, y es el tipo de optimización deseada en el problema")
    print("- 'Número de variables de decisión' es un entero, y es el número de variables del problema")
    print("- 'Número de restricciones' es un entero, y es el número de restricciones del problema")
    print("- 'coeficientes de la función objetivo' son valores numéricos separados por comas, y son los coeficientes")
    print("de la función objetivo")
    print("- 'coeficientes de la restricción' son valores numéricos separados por comas, y son los coeficientes")
    print("de la restricción")
    print("- 'signo de restricción' es un símbolo ['<=', '>=', '='], e indica el tipo de inecuación")
    print("- 'número en la derecha de la restricción' es un valor numérico, y es el número en la derecha de la restricción")
    print("\nNota: Se pueden añadir en distintas líneas tantas restricciones como las indicadas en 'Número de restricciones'")
    print("\n")
    print("##########################################################################################################")
    print("----------------------------------------------------------------------------------------------------------")
    print("Final Sección Ayuda")
    print("----------------------------------------------------------------------------------------------------------")
    print("##########################################################################################################")
    print("\n")
    
def inicializar_matriz():
    #Función que inicializa la matriz con ceros
    global matriz
    matriz=[] #Vaciar matriz
    
    for i in range(len(nombre_filas)): #Total de filas
        row=[] #Fila
        for j in range(len(nombre_columnas) - 1): #Total de columnas
            row.append(Fraccion(0,1)) #Añadir Fracción 0/1 para cada columna de esta fila
        matriz.append(row) #Añadir fila definida a la matriz

def menor_fraccion(lst):
    #Función que retorna el objeto fracción correspondiente al valor menor de una lista de fracciones
    menor = lst[0]
    for i in range(len(lst)):
        elem = lst[i]
        if (Fraccion.comparar(elem, menor)): # Si menor actual es mayor que el elem
            menor = elem

    return menor

def menor_coeficienteObjetivo():
    #Función que retorna la posición del coeficiente mínimo de la función objetivo,
    #lo que permite obtener la posición de la columna pivote
    res = copy.deepcopy(matriz[0])
    fila = res[:len(res)-1] # No se incluye la columna LD
    f = menor_fraccion(fila)
    return buscar_fraccion(fila, f) # Retorno la posición de la fracción en la columna

def buscar_fraccion(lst, f):
    #Función que retorna el índice de la posición de una fracción si la encuentra en la lista
    #En caso contrario retorna -1
    pos = -1
    for j in range(len(lst)):
        if ((lst[j].get_num() == f.get_num()) and (lst[j].get_denom() == f.get_denom())):
            pos = j
            break

    return pos
    
def imprimir_salida_alineamiento():
    # Función que imprime la salida del problema de alineamiento de secuencias
    try: #Abrir archivo de salida
        salida = open(str(nom_archivo) + '_respuesta', 'w')               
    except IOError:
        print ("Error: No se logró crear o sobrescribir el archivo\n")
    else:
        print ("Archivo creado o modificado exitosamente\n")
        
        if (algoritmo == 1): #(F.Bruta)
            
            for elem in resultados:
                if (elem[2] == scorefinal): # Imprimir sólo las comparaciones que empataron con el mejor puntaje
                    print("".join(elem[0]) + ", " + "".join(elem[1]) + ", " + str(elem[2])) # Imprimir en terminal
                    salida.write("".join(elem[0]) + ", " + "".join(elem[1]) + ", " + str(elem[2]) + "\n") # Guardar en archivo
                    
            print("") # Imprimir en terminal                
            print("Score Final: "+ str(scorefinal))
            print("Hilera1: "+ secuencia1)
            print("Hilera2: "+ secuencia2)                
            salida.write("\n") # Guardar en archivo 
            salida.write("Score Final: "+ str(scorefinal) + "\n")
            salida.write("Hilera1: "+ secuencia1 + "\n")
            salida.write("Hilera2: "+ secuencia2 + "\n")

        if (algoritmo == 2): #(P.Dinámica)
            salida.write("\n")
            
        salida.close() # Cerrar archivo

def puntajetotal(elem1, elem2):
    # Función que retorna el puntaje correspondiente a comparar 2 secuencias (Para el algoritmo de fuerza bruta)
    score = 0
    for i in range(len(elem1)):
        if (elem1[i] == elem2[i] and elem1[i] != '_'):
            score = score + 1
        elif (elem1[i] != elem2[i] and elem1[i] != '_' and elem2[i] != '_'):
            score = score - 1
        elif (elem1[i] == '_' and elem2[i] != '_'):
            score = score - 2
        elif (elem1[i] != '_' and elem2[i] == '_'):
            score = score - 2
        elif (elem1[i] == elem2[i] and elem1[i] == '_'):
            score = score - 4
    return score

def mejor_resultado():
    # Función que retorna una lista con la secuencia1 y la secuencia2 y la mayor puntuación
    resultado = copy.deepcopy(resultados[0])
    for i in range(len(resultados)):
        if (resultados[i][2] > resultado[2]):
            resultado = copy.deepcopy(resultados[i])
            
    return resultado           
    
############################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------
#MAIN
#---------------------------------------------------------------------------------------------------------------------------
############################################################################################################################     
def main():
    
    global matriz # Para trabajar con variables globales
    global salida
    global id_problema 
    global algoritmo
    global nom_archivo
    
    global secuencia1
    global secuencia2
    global scorefinal

    global resultados
    
    arg_valido = True

    if (len(sys.argv) == 2 and sys.argv[1] == "-h"): #Si hay opción -h
        arg_valido = False
        manual()

    elif (len(sys.argv) == 2 and sys.argv[1] != "-h"): #Si largo 2 pero no hay opción -h
        arg_valido = False
        print("\nPara ver 'ayuda' el argumento #2 debe ser '-h'\n")

    if (len(sys.argv) == 4): #Si el número de argumentos es igual a 4
        
        if (not(sys.argv[1].isnumeric() and sys.argv[2].isnumeric() and isinstance(sys.argv[3], str))): #Chequear tipos de argumento de línea de comandos
            print("\nTipo equivocado de argumentos (Para la 'resolución' se requiere: string int int string)\n")
            arg_valido = False # Tipos equivocados

    if (len(sys.argv) != 2 and len(sys.argv) != 4):
        arg_valido = False # Número equivocado de argumentos
        print("\nNúmero equivocado de argumentos (Para 'ayuda' se requieren 2, para la 'resolución' se requieren 4)\n")
        
        if (len(sys.argv) == 1): # Si no se agregaron argumentos además del nombre del programa
            print("Sólo se recibió el nombre del programa\n")

    if (arg_valido): #El número y tipo de los argumentos es válido
       id_problema = int(sys.argv[1]) # Obtener datos de línea de comandos
       algoritmo = int(sys.argv[2])
       nom_archivo = sys.argv[3]
        
       lineas = []
       try:
           entrada = open(sys.argv[3],"r")        
           lineas = entrada.readlines() # Obtiene todas las líneas del archivo de entrada        
       except IOError:
          print ("\nError: No se logró encontrar el archivo\n")
       else:
          print ("\nDatos extraídos exitosamente del archivo\n")
          entrada.close()
        
       for i in range(len(lineas)): # Quitar comillas de las lineas
           lineas[i] = lineas[i].split(',')

       if (id_problema == 1 and algoritmo == 1): # Mochila (F.Bruta)
           print("No implementado aún\n")
           
       if (id_problema == 1 and algoritmo == 2): # Mochila (P.Dinámica)
           print("No implementado aún\n")
           
       if (id_problema == 2): # Alineamiento de Secuencias
           secuencias = []          
           for line in lineas: # Obtener secuencias
               str1 = " "
               elem = str1.join(line)
               secuencias.append(elem.rstrip())

           secuencia1 = secuencias[0]
           secuencia2 = secuencias[1]
           
           if (algoritmo == 1): #(F.Bruta)
               mayor = len(secuencia2) # Guarda el largo de la secuencia de entrada más corta
               
               if (len(secuencia1) > len(secuencia2)):
                   mayor = len(secuencia1)
                   
               k = len(secuencia1) + len(secuencia2) # Obtener el número máximo de gaps
               
               resultados = [] # Contiene todas las comparaciones entre permutaciones y sus puntajes respectivos
               while (k >= mayor): # Probar con diferente número de gaps
                   gaps1 = k - len(secuencia1) # Obtener número de gaps a permutar
                   gaps2 = k - len(secuencia2)
                   perm1 = list(set(permutations(('A'*len(secuencia1)) + ('_'*gaps1)))) # Permutar largo de la secuencia (un mismo símbolo) + gaps, y remover permutaciones repetidas
                   cont = 0
                   for i in range(len(perm1)): # Sustituir símbolos repetidos por bases nitrogenadas de la secuencia1
                       perm1[i] = list(perm1[i]) # Convertir tupla a lista
                       for j in range(len(perm1[0])):
                           if (perm1[i][j] == 'A'):
                               perm1[i][j] = secuencia1[cont]
                               cont = cont + 1
                       cont = 0
                   perm2 = list(set(permutations(('A'*len(secuencia2)) + ('_'*gaps2)))) # Permutar largo de la secuencia (un mismo símbolo) + gaps, y remover permutaciones repetidas
                   cont = 0
                   for i in range(len(perm2)): # Sustituir símbolos repetidos por bases nitrogenadas de la secuencia2
                       perm2[i] = list(perm2[i]) # Convertir tupla a lista
                       for j in range(len(perm2[0])):
                           if (perm2[i][j] == 'A'):
                               perm2[i][j] = secuencia2[cont]
                               cont = cont + 1
                       cont = 0
                   for elem1 in perm1: # Comparar las secuencias obtenidas de cada permutación
                       for elem2 in perm2:
                           puntaje = puntajetotal(elem1, elem2) # Obtener el puntaje de la comparación de 2 secuencias 
                           resultado = [elem1, elem2, puntaje]
                           resultados.append(resultado) # Guardar las secuencias que se compararon y el puntaje respectivo
                           
                   k = k - 1                       
#                   print("Permutaciones secuencia1 con gaps="+str(gaps1)) # Imprimir las permutaciones con distinta cantidad de gaps
#                   for i in perm1:
#                       print(i)
#                   print("Permutaciones secuencia2 con gaps="+str(gaps2))
#                   for i in perm2:
#                       print(i)

                       
               resfinal = mejor_resultado() # Obtener el alineamiento con el mayor puntaje
               secuencia1 = "".join(resfinal[0])
               secuencia2 = "".join(resfinal[1])
               scorefinal = resfinal[2]
                   
               imprimir_salida_alineamiento() # Guardar en archivo de salida 
               
           if (algoritmo == 2): #(P.Dinámica)
               print("No implementado aún\n")


    #Imprimir datos de línea de comandos
    n = len(sys.argv) 
    print("\nTotal de argumentos pasados:", n) 
  
    print("\nArgumentos pasados:", end = " ") 
    for i in range(0, n): 
        print(sys.argv[i], end = " ")
    print("\n")


if __name__ == "__main__":
    main()