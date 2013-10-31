# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:46:55 2013

@author: Anand

All the calculation for the diaphragm deflection and stress using Roarks formulae
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
    K_1 = 5.33/(1 - diaphragm.mu**2)
    K_2 = 2.6/(1- diaphragm.mu**2)
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
    
def sigmaRmax(y0, diaphragm):
    """
    Returns the maximum radial stress in the diaphragm
    
    y0: maximum deflection of the diaphragm
    diaphragm: Diaphragm class object used
    
    """
    K_3 = 2/(1- diaphragm.mu)
    K_4 = 0.976
    return diaphragm.E * diaphragm.h**2 / diaphragm.a**2 *(K_3 * y0 / diaphragm.h + K_4 * y0**2 / diaphragm.h**2)
    
def sigmaEdge(y0, diaphragm):
    """
    Returns the stress at the edge of the diaphragm
    
    y0: maximum deflection of the diaphragm
    diaphragm: Diaphragm class object used
    """
    K_3 = 4 / (1- diaphragm.mu**2)
    K_4 = 1.73
    return diaphragm.E * diaphragm.h**2 / diaphragm.a**2 *(K_3 * y0 / diaphragm.h + K_4 * y0**2 / diaphragm.h**2)

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

def plotPvsSigmaRmax(P, diaphragm):
    """
    Plots graph of pressure vs maximum radial stress which is at the center of the diaphragm
    
    P: Numpy array of pressure[Pa]
    diaphragm: diaphragm used
    """
    y = tensileBendingDeflect(P, diaphragm)
    sigmaR = sigmaRmax(y, diaphragm)
    plt.title("Pressure vs maximum radial stress[Pa]")
    graph(P, sigmaR, "Pressure[Pa]", "Stress[Pa]", diaphragm.name)

def plotPvsSigmaEdge(P, diaphragm):
    """
    Plots grapg of pressure vs stress at the edge
    
    P: Numpy array of pressure[Pa]
    diaphragm:diaphragm used
    """
    y = tensileBendingDeflect(P, diaphragm)
    sigma = sigmaEdge(y, diaphragm)
    plt.title("Pressure vs edge stress")
    graph(P, sigma, "Pressure[Pa]", "Stress[Pa]", "Edge stress")


if __name__ == "__main__":
    P_max = 6e5
    P = np.arange(0,P_max,P_max/1000.0)
    plt.close('all')
    diaph = [diaphNB40_50, diaphNB25, diaphNB15_20]
    for diaphUsed in diaph:
        y = tensileBendingDeflect(P, diaphUsed)
        plt.figure(diaphUsed.name)
        Syt = diaphUsed.Syt * np.ones((len(P), 1))
        #diaphragm yield strength
        plotPvsSigmaRmax(P, diaphUsed)
        maxShear = Syt / 2.0
        #diaphragm maximum shear stress
        graph(P, maxShear, "Pressure[Pa]", "Stress[Pa]", "Maximum shear stress")
        #maximum radial stress which is at the center
        plotPvsSigmaEdge(P, diaphUsed)
    