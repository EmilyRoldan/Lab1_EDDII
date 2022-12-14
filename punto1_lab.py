# -*- coding: utf-8 -*-
"""Punto1_LAB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nuwqElx-1DVt8Mga5xXOq4zI6uewnxk_
"""
#Clase Nodo para la creación de árboles
class Node:
  def __init__(self , data):
    self.data = data
    self.l = None
    self.r = None
#Clase para obtener los caminas a las hojasy así saber la altura
class Caminos:
  def __init__(self):
    self.data = []

#Función que obtiene todos los caminos de un nodo hasta una hoja en forma de lista
def recorridos(tree, caminos, aux):
  if tree:
        aux.data.append(tree.data)
        recorridos(tree.l, caminos, aux)
        recorridos(tree.r, caminos, aux)

        if tree.l == tree.r:
          caminos.data.append(aux.data.copy())
        aux.data.pop(-1)

#Obtiene el mayor tamaño de las listas obtenidas anteriormente
def mayor_distancia(caminos):
  mayor = 0
  for x in caminos.data:
    if len(x) > mayor:
      mayor = len(x)
  return mayor

#Unifica las dos funciones anteriores para mayor facilidad
def altura(tree):
  if tree == None:
    return 0
  
  caminos = Caminos()
  aux = Caminos()
  recorridos(tree, caminos, aux)
  return mayor_distancia(caminos)

#Funciones que realizan las rotaciones de los árboles
def rot_si(node):
  hijo = node.l
  node.l = hijo.r
  hijo.r = node
  return hijo

def rot_sd(node):
  hijo = node.r
  node.r = hijo.l
  hijo.l = node
  return hijo

def rot_di(node):
  node.l = rot_sd(node.l)
  return rot_si(node)

def rot_dd(node):
  node.r = rot_si(node.r)
  return rot_sd(node)

#Función para obtener el padre de un nodo teniendo en cuenta que es un BST
def padre(Root, data):
    if data == None:
      return data

    data = data.data
    P = Root
    AP = None
    while True:
      if P:
        if P.data == data:
          return AP
        elif data < P.data:
          AP = P
          P = P.l
        else:
          AP = P
          P = P.r
      else:
        return None

#Función para obtener el abuelo de un nodo
def abuelo(Root, data):
  return padre(Root, padre(Root, data))


#Función para obtener el tío (el hijo del abuelo que no es el papá del nodo)
def tio(Root, data):
  aux = abuelo(Root, data)

  if aux.l.l.data == data or aux.l.r.data == data:
    return aux.r
  else:
    return aux.l

#Función para buscar un nodo en el árbol teniendo en cuenta que es un BST
def search(Root, data):
    if data == None:
      return data
    P = Root
    while True:
      if P:
        if P.data == data:
          return P
        elif data < P.data:
          P = P.l
        else:
          P = P.r
      else:
        return None

#Función auxiliar para modificar las conexiones del padre al hijo a eliminar
def dele(Root, data, new):
  aux1 = padre(Root, data)
  if aux1 == None:
    Root = new
  elif aux1.l == data:
    aux1.l = new
  else:
    aux1.r = new

#Función que elimina los nodos
def delete(Root, data):
  
  node = search(Root, data)
  aux1 = padre(Root, node)

  #Si el nodo no tiene hijos, simplemente se borra (es una hoja)
  if node.l == None and node.r == None:
    dele(Root, node, None)
    res = verify(aux1, Root)
  #Si no tiene hijo izquierdo, el subarbol derecho sube a la posición del que se elimina
  elif node.l == None:
    dele(Root, node, node.r)
    res = verify(aux1, Root)
  elif node.r == None:
    dele(Root, node, node.l)
    res = verify(aux1, Root)
  
  #Si tiene ambos hijos, se busca el menor del subarbol derecho y toma el lugar del que se eliminará
  else:
    aux = minimo(node.r)
    aux2 = padre(Root, minimo(node.r))
    temp = aux.data
    delete(Root, aux.data)
    node.data = temp
    res = verify(aux2, Root)

  #Para todos los casos se verifica que los nodos superiores(los afectados por la eliminación) y el árbol en general quede balanceado
  return res

#Obtiene el elemento mínimo de un árbol
def minimo(Root):
  P = Root
  AP = None
  while P != None:
    AP = P
    P = P.l
  return AP

#Inserta un nodo a un árbol, teniendo en cuenta que es un BST
def insert_node(Root, data):
  if Root == None:
    return Node(data)
  else:
    aux = True
    P = Root
    while aux:
      if data < P.data:
        if P.l == None:
          P.l = Node(data)
          aux = False
        else:
          P = P.l
      elif data > P.data:
        if P.r == None:
          P.r = Node(data)
          aux = False
        else:
          P = P.r
      else:
        aux = False

    res = verify(P, Root)
    return res

#Función que se encarga de balancear el árbol, dependiendo de los factores de equilibrio
def balancear(node):
    if altura(node.l) - altura(node.r) == 2:
      if altura(node.l.l) >= altura(node.l.r):
         return rot_si(node)
      else:
        return rot_di(node)
    if altura(node.r) - altura(node.l) == 2:
      if altura(node.r.r) >= altura(node.r.l):
         return rot_sd(node)
      else:
        return rot_dd(node)

#verifica que los nodos superiores(los afectados por la eliminación) y el árbol en general quede balanceado
def verify(node, Root):
  P = node
  AP = None
  while P != None:
      aux2 = padre(Root, P)
      if aux2 == None:
        b = 0
      elif aux2.r == P:
        b=1
      else:
        b=2
      aux = balancear(P)
      if aux != None:
        if b == 0:
          P = aux
        elif b ==1:
          aux2.r = aux
        else:
          aux2.l = aux
      AP = P
      P = aux2
  return AP

#Llama a la fucnión recursiva el mismo número de veces que de niveles o altura tenga el árbol 
def level_order(Root):
  h = altura(Root)
  for i in range(1, h+1):
    nivel_actual(Root, i)
  

def nivel_actual(Root, level):
  if Root:
    #Solo va a escribir cuando  la cuenta atrás del contador llegue a 1
    if level == 1:
      print(Root.data, end=" ")
    else:
      #Va a bajar level-1 niveles hasta llegar a aquel por el que no se ha pasado (El for de la función anterior permite esto).
      nivel_actual(Root.l, level-1)
      nivel_actual(Root.r, level-1)


#---------------------------------------------------------Ejemplo
Root = None
Root = insert_node(Root, 5)
Root = insert_node(Root, 10)
Root = insert_node(Root, 15)
Root = insert_node(Root, 3)
Root = insert_node(Root, 2)
Root = insert_node(Root, 1)
Root = insert_node(Root, 7)
Root = insert_node(Root, 9)
Root = delete(Root, 3)

level_order(Root)