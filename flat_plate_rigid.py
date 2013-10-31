# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 14:47:17 2013

@author: anand
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from data_diaphragm import *

def maxsigmaR(P, flatPlate):
    """
    Returns the radial stress in a membrane
    r: distance from the center of the diaphragm
    y0: maximum deflection
    diaphragm: diaphragm used
    """
    try:
        return 3 * P / (4 * flatPlate.h**2) * (flatPlate.a**2 - flatPlate.b)
    except ZeroDivisionError:
        return None

def plotPvsSigmaR(P, flatPlate):
    """
    Plot a graph of pressure vs. maximum radial stress in the flat plate using
    flat plate theory
    """
    sigmar = [maxSigmaR(p, flatplate) for p in P]
    graph(P, sigmar, "Pressure[Pa]", "Maximum Radial Stress[Pa]")

def plotPvsSigmaT(P, flatPlate):
    """
    Plot a graph of pressure vs. maximum radial stress in the flat plate using
    flat plate theory
    """
    sigmat = [maxSigmaT(p, flatplate) for p in P]
    graph(P, sigmat, "Pressure[Pa]", "Maximum Tangential Stress[Pa]")

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    
def calcAp(flatPlate):
    """(diaphragm class object) -> float
    Returns the coefficient Ap in the characteristic equation of flat diaphragm
    with rigid center
    """
    return 3 * (1 - flatPlate.mu**2) / 16.0 * (1 - (flatPlate.b/flatPlate.a)**4 - 4.0 * (flatPlate.b/flatPlate.a)**2 * math.log(flatPlate.a/ flatPlate.b))

def rigidPlateDeflect(r, P, flatPlate):
    """
    Returns the deflection for given flat plate with following parameters
    
    r: distace from the center of flat plate
    flatPlate: flatPlate used
    """
    Ap = calcAp(flatPlate)
    return Ap * P * flatPlate.a**4 / (flatPlate.E * flatPlate.h**3)


def detDeflect(P, flatPlate):
    """
    Returns a list of maximum values of deflection in mm for given applied pressure values
    
    P: list of pressure
    """
    return [rigidPlateDeflect(0, p, flatPlate) for p in P]
    
def plotPvsy(P, flatPlate, legend):
    """
    Plots the graph of deflection variation with pressure variation for given flatPlate
    
    P: list of pressure values
    """
    y = detDeflect(P, flatPlate)
    graph(P, y, "Pressure[Pa]", "Deflection[m]", legend = legend)

if __name__ == "__main__":
    #plt.close("all") # close all previous figures
    P_max = 4 * 10**5
    P = np.arange(0,P_max,P_max/1000.0 )
    #Consideration of only tensile stresses
    plt.figure("Flat diaphragm:P vs. y using flat plate theory")
    plotPvsy(P, diaphNB40_50_rigid, "Diaphragm 40 and 50NB")
    plotPvsy(P, diaphNB15_20_rigid, "Diaphragm 15 and 20NB")
    plotPvsy(P, diaphNB25_rigid, "Diaphragm 25NB")
    
