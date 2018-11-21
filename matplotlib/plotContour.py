# -*- coding: utf-8 -*-
"""
plotContour function demo

Created on Sun Mar 27 23:49:09 2016
@author: Addis
"""

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np


def plotContour(x,y,z,Nlevel,cmapName='PiYG'):
    # x and y are bounds, so z should be the value *inside* those bounds.
    # Therefore, remove the last value from the z array.
    z = z[:-1, :-1]
    levels = MaxNLocator(nbins=Nlevel).tick_values(z.min(), z.max())
    
    # pick the desired colormap, sensible levels, and define a normalization
    # instance which takes data values and translates those into levels.
    cmap = plt.get_cmap(cmapName)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    
    fig, ax1 = plt.subplots(nrows=1)
    
    # im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm)
    # fig.colorbar(im, ax=ax0)
    # ax0.set_title('pcolormesh with levels')
    
    # contours are *point* based plots, so convert our bound into point
    # centers
    cf = ax1.contourf(x[:-1, :-1],
                      y[:-1, :-1], z, levels=levels,
                      cmap=cmap)
    fig.colorbar(cf, ax=ax1)
    ax1.set_title('contourf with levels')
    
    # adjust spacing between subplots so `ax1` title and `ax0` tick labels
    # don't overlap
    fig.tight_layout()
    
    plt.show()

x=np.linspace(-2,2,100);
y=x;
x,y=np.meshgrid(x,y)
z=np.sin(x**2+y**2)/(x**2+y**2+1e-10)
plotContour(x, y, z, 100, 'winter')