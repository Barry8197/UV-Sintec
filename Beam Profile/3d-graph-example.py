# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:16:33 2019

@author: Morrison-Lab
"""
#from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

def z_function(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = z_function(X, Y)

#fig = plt.figure()
#ax = plt.axes(projection="3d")
#ax.plot_wireframe(X, Y, Z, color='green')
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#ax.set_zlabel('z')

#plt.show()


noofangles = 12
X1 = np.zeros((noofangles,399))
Y1 = np.zeros((noofangles,399))
Z1 = np.zeros((noofangles,399))

input_angles = np.arange(0, 181, 180/noofangles)

angle = np.arange(-89.55, 90, 0.45) 
anglex = angle
for difAngle in range (0, noofangles+1):
    Z1[difAngle] = np.cos(np.deg2rad(angle))
    X1[difAngle] = angle*np.cos(np.deg2rad(input_angles[difAngle]))
    Y1[difAngle] = angle*np.sin(np.deg2rad(input_angles[difAngle]))

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_wireframe(X1, Y1, Z1, color='red')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

