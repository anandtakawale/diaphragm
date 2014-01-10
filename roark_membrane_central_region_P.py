# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:19:34 2013

@author: Anand

Pressure applied on the center region of the diaphragm - using Roark's formula
"""

from data_diaphragm import *
import numpy as np
import matplotlib.pyplot as plt


def tensileBendingDeflect(P, diaphragm):
    """
    Returns the deflection for given value of pressure
    The formula used is form Roark's formula for stress and strain
    circular plate with fixed and held with uniform pressure over the entire plate
    
    P: Pressure in Pa
    diaphragm: Diaphragm class object used
    
    """
    K_1 = 9.17
    K_2 = 5.5
    coeff = np.zeros((len(P), 4))
    #coefficient for the y^3
    coeff[:,0] = K_2 / diaphragm.h**3
    #coefficient for y^2 is already 0.0
    #coefficient for y
    coeff[:,2] = K_1 / diaphragm.h
    coeff[:,3] = -P * diaphragm.a**4/(diaphragm.E * diaphragm.h**4)
    realRoot = np.zeros((len(P), 1))
    for i in range(len(P)):    
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
    plt.legend(loc = 'best')

def plotPvsy(P, diaphragm, legend = "", color = ""):
    """
    Plots graph of pressure vs deflection for the given diaphragm
    
    P: Numpy array of pressure[Pa]
    diaphragm: diaphragm used
    """
    y = tensileBendingDeflect(P, diaphragm)
    graph(P, y * 1e3, "Pressure[Pa]", "Deflection[mm]", legend, color)


if __name__ == "__main__":
    P_max = 5e5
    P = np.arange(0,P_max,P_max/1000.0)
    plt.close('all')
    diaph = [diaphNB40_50, diaphNB25, diaphNB15_20]
    for diaphUsed in diaph:
        plotPvsy(P, diaphUsed, diaphUsed.name)