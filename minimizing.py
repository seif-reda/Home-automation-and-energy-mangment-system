# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:44:13 2020

@author: Haddad
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import random
import cvxpy as cp




prices = [29,22.07,20.75,17.61,18.29,21.39,23.47,26.75,34.09,35.8,35.39,45.56,\
          43.52,58.03,70.57,88.57,99.02,91.23,71.46,43.53,49.45,35.32,34.57,31.38]
DAP =  [x * 0.001 for x in prices]
# start=1
# end=24
# list = list(range(start,end+1))
# # plt.plot(list, PRICES)
# plt.title("Prices per hour") 
# plt.xlabel("hour") 
# plt.ylabel("price") 
# plt.show() 

EaMax = 0.5
E_a = np.array([[1.2282], [0.3], [0.1577], [0.846], [1.46]])    # energy consumption per device
a_a = np.array([[7], [10], [17], [9], [18]])                    # starting time of each appliance
b_a = np.array([[23], [11], [19], [13], [23]])                  # ending time of each appliance
x_a = np.array([[0.0514], [0], [0], [0], [0]])                  # min allowed power
y_a = np.array([[0.14], [0.3], [0.1], [0.3], [0.54]])           # max allowed power per appliance
D_a = np.array([[0], [1], [2], [2], [1]])                       # duration of each device


# required variable to be optimized
x_des = cp.Variable((5,24)) # the new energy consumption schedule matrix
hourlyLoad = 0              # to keep track of hourly load consumbtion for all appliance
constraints= []              # contstrains to solve about

# looping in the array of the usage of all devices, each per hour 
# and defining max and min limits for each appliance over the 24 hours
for i in range( x_des.shape[0]):
    for j in range(x_des.shape[1]):
        constraints += [ x_a[i] <= x_des[i][j], x_des[i][j]<= y_a[i], ]

# settin the max hourly load to be less than or equal the 
# hourly load limit
for j in range(x_des.shape[1]):
    for i in range( x_des.shape[0]):
        hourlyLoad += x_des[i][j]
    constraints += [hourlyLoad <= EaMax]



objective = cp.Minimize(cp.sum(cp.multiply(DAP, cp.sum(x_des))))
prob = cp.Problem(objective, constraints)
result = prob.solve()








