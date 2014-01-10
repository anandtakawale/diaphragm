# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:21:05 2013

@author: Anand
"""
from data_diaphragm import *
import numpy as np
import matplotlib.pyplot as plt

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend, lw = 2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    plt.grid()

def tensileBendingDeflect(P, diaphragm):
    """
    Returns the deflection values for the given pressure for the convex diaphragm specified
    P: Pressure [Pa] numpy array
    diaphragm: convex diaphragm used [object of convexdiaphragm class]
    """
    coeff = np.zeros((len(P), 4))
    #coefficient for y^3
    coeff[:, 0] = 2.76 / diaphragm.h**3
    #coefficient for y^2
    coeff[:, 1] = - 7.72 * diaphragm.A/diaphragm.h / diaphragm.h**2
    #coefficient for y
    coeff[:, 2] = 5.86 + 4.88 * (diaphragm.A/diaphragm.h)**2 / diaphragm.h
    #constant value
    coeff[:, 3] = - P * diaphragm.a**4 / ( diaphragm.E * diaphragm.h**4)
    realroots = np.zeros((len(P), 1))
    for i in range(len(P)):
        roots = np.roots(coeff[i, :])
        for root in roots:
            if root.imag == 0:
                realroots[i, 0] = root.real
    return realroots

def plotPvsyTensileBending(P, diaphragm, legend, color = ""):
    """
    Plots the pressure vs. deflection curve considering tensile and bending.
    
    P: list contaning variable pressures
    legend: legend for the plot
    """
    #diaphragm properties
    deflect = tensileBendingDeflect(P, diaphragm) * 1e3
    graph(P * 1e-5, deflect, "Pressure(bar)", "Deflection(mm)", legend, color)


if __name__ == "__main__":
    plt.close("all") # close all previous figures
    P_max = 1 * 1e5
    P = np.arange(0,P_max + P_max / 2000.0,P_max/2000.0)
    diaphragms = [diaphNB40_50_convex, diaphNB40_50_convex_double]
    for diaph in diaphragms:
        plotPvsyTensileBending(P, diaph, diaph.name, '-')
    plt.figure()
    plotPvsyTensileBending(P, diaphNB20_convex, diaphNB20_convex.name, '-')
    plt.figure()
    plotPvsyTensileBending(P, diaphNB20_double_convex, diaphNB20_double_convex.name, '-')
    plt.figure()
    
    plt.show()