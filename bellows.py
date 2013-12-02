# -*- coding: utf-8 -*-
"""
Created on Mon Dec 02 14:16:35 2013

@author: Anand
"""
import matplotlib.pyplot as plt
import numpy as np
import data_diaphragm

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')

def tensileBendingDeflect(P, diaphragm):
    """
    Returns the deflection considering tensile as well as bending stresses
    
    P:Pressure in [Pa] numpy array
    
    All parameters follow same system of units(SI).
    """
    coeff = np.zeros((len(P), 4))
    #coefficiet of y**3
    coeff[:,0] = diaphragm.Bp / diaphragm.h**3
    #coefficient of y**2 is already made zero
    #coefficient of y
    coeff[:,2] = 1.0/ (diaphragm.Ap * diaphragm.h)
    #coefficient constant
    coeff[:,3] = -P * diaphragm.a**4 / (diaphragm.E * diaphragm.h**4)
    realRoot = np.zeros((len(P), 1))
    for i in range(len(P)):
        roots = np.roots(coeff[i,:])
        for root in roots:
            if root.imag == 0:
                realRoot[i,0] = root.real
    return realRoot

def plotPvsyTensileBending(P, diaphragm, legend, color = ""):
    """
    Plots the pressure vs. deflection curve considering tensile and bending.
    
    P: list contaning variable pressures
    legend: legend for the plot
    """
    #diaphragm properties
    deflect = tensileBendingDeflect(P, diaphragm) * 1e3
    graph(P * 1e-5, deflect, "Pressure(Pa)", "Deflection(mm)", legend, color)

if __name__ == "__main__":
    P = np.arange(0, P_max + P_max/1000.0, P_max/1000.0)
    plotPvsyTesileBending(P, BT6, BT6.name)