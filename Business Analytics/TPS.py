# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:46:40 2022

@author: PTL14736
"""

# Travelling Salesman Problem: TSP
"""
a: tuple, ex (12.0 , 30.0)
b: tuple, ex (54.0, 60.1)

A(xA, yA) e B (xB, Yb)
dAB² =(xB – xA)² + (yB – yA)²
"""

import matplotlib.pyplot as plt
import os
from scipy.spatial import distance_matrix
import pandas as pd
import math

def dist_between_two_points(a, b):

    dist = math.sqrt(((a[0]-b[0])**2)+(a[1]-b[1])**2)
    return dist

dist_between_two_points([12.0, 30.0], [54.0, 60.1])


route = [1, 23, 34, 1]
len(route)
for i in range(len(route)-1):
    print(route[i])
    print(route[i], route[i+1])  # 1, 23; 23, 34; 34,1, depois dá erro

for i in range(4):
    print(i)

for i in range(3):  # por isso é que temos -1
    print(i, i+1)



os.chdir('C:/Users/PTL14736\OneDrive - KME/Documents/Milene/DSBA/4.Business Analytics/')


locations = pd.read_table('berlin52.tsp', skiprows=6, skipfooter=1, sep=' ', names=(
    'location_id', 'x', 'y'), engine='python')
locations = locations.set_index('location_id')

print(locations)

plt.plot(locations.x, locations.y, 'o')


dist_mat = pd.DataFrame(distance_matrix(locations[['x', 'y']], locations[['x', 'y']]),
                        index=locations.index,
                        columns=locations.index)  # calculamos o distance matrix e depois convertemos num panda dataframe
print(dist_mat)

"""
route: list with the ordered point indexes. Ex: [1, 23, 47, 21, ..., 1]
dist_mat: DataFrame
"""


def total_distance(route, dist_mat):

    total_dist = 0

    for i in range(len(route)-1):
      this_distance = dist_mat[route[i]][route[i + 1]]
      total_dist += this_distance

    return total_dist


res = total_distance(route, dist_mat)
print(res)


def build_initial_solution(dist_mat, start_and_finish_point=1):
    route = []
    route.append(start_and_finish_point)
    
    point=start_and_finish_point 
    while len(route) < len(dist_mat.columns):
       next_point = dist_mat[point].loc[[p not in route for p in dist_mat.columns]].idxmin()
       point = next_point 
       route.append(next_point)
       
    route.append(start_and_finish_point) #fecha a route
    return route

init_solution = build_initial_solution(dist_mat)
print(len(init_solution))
print(init_solution[0])
print(init_solution[-1])
init_solution 

print(init_solution)

def swap_2opt(route, i, k):
    assert i >= 0 and i < (len(route) - 1)
    assert k > i and k < len(route)
    new_route = route[0:i]
    new_route.extend(reversed(route[i:k + 1]))
    new_route.extend(route[k+1:])
    assert len(new_route) == len(route)
    return new_route

swap_2opt(route,0,1)

#qual é a distância total route?
#selecionar i e k e chamar a função swap_2opt para obter uma nova rota 
#nova rota é melhor do que a rota atual? 
    #se sim, o que tenho que fazer?
    #se não, avançar para a próxima combinação de i e k
    #como é que itero sobre todas as combinações de i e k? 
    #quando encontro uma rota melhor, tenho de voltar a iterar sobre todas as combinações de i e k até encontrar uma rota melhor
   #quando itera

def local_search(route, dist_mat):
  # Qual é distância total de route?
  best_distance = total_distance(route, dist_mat)
  best_route = route
  # Selecionar um i um k e chamar a função swap_2opt para obter uma nova rota?
  def iterator(best_route, best_distance):
    for i in range(1, len(route) - 2):
      for k in range(i + 1, len(route) - 1):
        new_route = swap_2opt(best_route, i, k)
        new_distance = total_distance(new_route, dist_mat)
        if new_distance < best_distance:
          best_route = new_route
          best_distance = new_distance
          return best_route, best_distance
    return None, None

  while True:
    new_route, new_distance = iterator(best_route, best_distance)
    print(new_distance)
    if new_route is None:
      return best_route
    else:
      best_route = new_route
      best_distance = new_distance

local_search(init_solution, dist_mat)

import matplotlib.pyplot as plt 
def plot_route(route):
    r = dict()
    r['location_id'] = route
    r['x'] = list()
    r['y'] = list()
    
    for location in route:
        r['x'].append(locations.x[location])
        r['y'].append(locations.y[location])
        
    df = pd.DataFrame(r)
    df = df.set_index('location_id')
    
    return plt.plot(df.x, df.y, '-o')   

plot_route(init_solution)

best_route = local_search(init_solution, dist_mat)
plot_route(best_route)


