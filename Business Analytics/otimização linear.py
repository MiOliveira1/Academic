# -*- coding: utf-8 -*-
"""
Business Analytics 

Created on Wed Oct 19 20:10:44 2022

@author: mioliveira
"""

#exemplo 3.1. 
import scipy.optimize as sp

c = [-500, -400]
A = [
     [1, 1.5], 
     [2, 1]
     ]
b = [75, 100]

res = sp.linprog (c, A_ub=A, b_ub=b, method='revised simplex')
print(res)


#exercicio 3.1.
"""" função objetivo: 500x1 + 400x2 + 280x3 
    castanheiro: x1 + 1,5x2 + 1,5x3 <= 75
    ébano: 2x1 + x2 + x3 <=100
    tempo: 2x1 + 2x2 + x3 <= 80
"""

import scipy.optimize as sp 

c=[-500,-400,-280]
A=[
   [1,1.5,1.5],
   [2,1,1],
   [2,2,1]
   ]
b=[75,100,80]

res= sp.linprog (c, A_ub=A, b_ub=b, method='revised simplex' )
print(res)




