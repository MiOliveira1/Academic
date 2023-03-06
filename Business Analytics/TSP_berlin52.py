# -*- coding: utf-8 -*-
"""
TSP - de acordo com a sebenta 

Created on Fri Oct 21 17:03:04 2022

@author: Mioliveira 
"""

import os 
os.chdir('C:/Users/PTL14736\OneDrive - KME/Documents/Milene/DSBA/4.Business Analytics/')

import pandas as pd

locations = pd.read_table('berlin52.tsp', skiprows=6, skipfooter=1, sep=' ', names=('location_id', 'x', 'y'), engine='python')
locations = locations.set_index('location_id')

print(locations) #52 pontos 

import matplotlib.pyplot as plt 
plt.plot(locations.x, locations.y, 'o') 

import scipy as sp
import numpy as np
    
from scipy.spatial import distance_matrix
dist_mat = pd.DataFrame(distance_matrix(locations[['x', 'y']], locations[['x', 'y']]),
                        index=locations.index,
                        columns=locations.index)
print(dist_mat) #distâncias entre os 52 pontos 


def build_initial_solution (dist_mat, start_and_finish_point=1):
    route=list()    
    route.append(start_and_finish_point)
    
    for point in dist_mat.columns:
        potencial_next_points = dist_mat[point].loc[[p not in route for p in dist_mat.columns]]
        try:
            next_point = potencial_next_points.idxmin()
            route.append(next_point)
        except ValueError:
            break 
    route.append(start_and_finish_point) #closing the cycle 
    return route 

def total_distance(route, dist_mat):
    total_dist = 0 
    
    for i, point in enumerate(route):
        try: 
            next_point = route[i + 1]
        except IndexError:
            break 
        total_dist += dist_mat[point][next_point]
    return total_dist 

def swap_2opt (route, i, k):
    assert i >= 0 and i < (len(route)-1)
    assert k > i and k < len(route)
    new_route = route[0:i]
    new_route.extend(reversed(route[i:k+1]))
    new_route.extend(route[k+1:])
    assert len(new_route) == len(route)
    return new_route 

def local_search(route):
    improvement = True 
    best_route = route 
    best_distance = total_distance(route, dist_mat)
    while improvement:
        improvement = False 
        for i in range(1, len(best_route)-2):
            for k in range(i+1, len(best_route)-1):
                new_route = swap_2opt(best_route, i, k)
                new_distance = total_distance(new_route, dist_mat)
                if new_distance < best_distance:
                    best_distance = new_distance 
                    best_route = new_route 
                    improvement = True 
                    break 
            if improvement: 
                break  
        assert len(best_route) == len(route)
        return best_route 
    
r = build_initial_solution(dist_mat)
print(f"total distance inicial solution: {total_distance(r,dist_mat)}")
r = local_search(r)
print(f"total distance final solution: {total_distance(r,dist_mat)}")                

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

best_route = local_search(r)
plot_route(best_route)                                             


