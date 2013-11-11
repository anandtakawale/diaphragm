# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:30:05 2013

@author: Admin
"""

from data_diaphragm import *
import numpy as np
import matplotlib.pyplot as plt


def tensileBendingDeflect(F, diaphragm, A, B):
    """
    Returns the deflection for given value of pressure
    The formula used is from Timoshinko
    circular plate loaded at the center
    
    F: Force in N
    diaphragm: Diaphragm class object used
    A: coefficient for linear term from table 83 in book
    B: coefficient for force term
    """
    coeff = np.zeros((len(F), 4))
    #coefficient for the y^3
    coeff[:,0] = A / diaphragm.h**3
    #coefficient for y^2 is already 0.0
    #coefficient for y
    coeff[:,2] = 1.0 / diaphragm.h
    coeff[:,3] = -B * F * diaphragm.a**2/(diaphragm.E * diaphragm.h**4)
    realRoot = np.zeros((len(F), 1))
    for i in range(len(F)):    
        roots = np.roots(coeff[i,:])
        for root in roots:
            if root.imag == 0:
                realRoot[i] = root.real
    return realRoot
    
def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend(loc = 'best')

def plotPvsy(P, diaphragm, legend = "", color = ""):
    """
    Plots graph of pressure vs deflection for the given diaphragm
    
    F: Numpy array of force[N]
    diaphragm: diaphragm used
    """
    y = tensileBendingDeflect(P, diaphragm, 0.443, 0.217)
    graph(F, y * 1e3, "Force[N]", "Deflection[mm]", legend, color)


if __name__ == "__main__":
    F_max = 5e2
    F = np.arange(0,F_max,F_max/1000.0)
    plt.close('all')
    diaph = [diaphNB40_50, diaphNB25, diaphNB15_20]
    for diaphUsed in diaph:
        plotPvsy(F, diaphUsed, "Pressure vs y" + str(diaphUsed.name))