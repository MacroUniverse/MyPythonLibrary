# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 02:14:39 2016

@author: Addis
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np


def plot3D(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
    linewidth = 0, antialiased = False)
    # ax.set_zlim(0, 1.01)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
    
x=np.linspace(-2,2,100);
y=x;
x,y=np.meshgrid(x,y)
z=np.sin(x**2+y**2)/(x**2+y**2+1e-10)
plot3D(x, y, z)