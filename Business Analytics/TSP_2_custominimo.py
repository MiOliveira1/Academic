# -*- coding: utf-8 -*-
"""

Travel Salesman Problem 

https://www.youtube.com/watch?v=dG3o1pw2Kzc 

Created on Thu Oct 20 18:23:39 2022

@author: Mioliveira 
"""

from sys import maxsize
v = 4 #número de pontos 

#definir a função travelling salesman funcition - calcula só o caminho, depois temos que definir funções para calcular o mínimo 
def travelling_salesman_function(graph,s):
    vertex = []
    for i in range(v):
        if i != s:
            vertex.append(i)
    
    min_path = maxsize 
    while True: 
        current_cost = 0 #poderiamos calcular a current_dist (distância) mas neste exemplo estamos a ver os custos 
        k = s 
        for i in range (len(vertex)):
            current_cost += graph[k][vertex[i]] #os custos vão incrementando 
            k = vertex [i] 
        current_cost += graph[k][s]
        min_path = min( min_path, current_cost) #otimizar o mínimo calculado 
        
        #função que nos dará o min_path se existir outro min_path 
        if not next_perm(vertex):
            break 
    return min_path 

def next_perm(l):
    n = len(l)
    i = n-2 
    
    while i >= 0 and l[i] > l [i+1]:
        i -= 1
        
    if i == -1:
        return False 
    
    j = i+1 #estamos a definir o caminho 
    while j <  n and l[j] > l[i]:
        j += 1
        
    j -= 1 
    
    l[i], l[j] = l[j], l[i]
    left = i+1
    right = i-1
    
    while left < right:
        l[left],l[right] = l[right],l[left]
        left += 1
        right -= 1
    return True 
        
#coordenadas do sistema com 4 pontos (distâncias entre eles)
graph = [[0, 10, 15, 20], [10,0,35,25], [15,35,0,30],[20,25,30,0]]
s = 0 #starting point 
res = travelling_salesman_function(graph,s)
print(res)