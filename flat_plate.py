# -*- coding: utf-8 -*-
"""
Created on Tue Sep 03 11:50:09 2013

Flat plate theory calculatios
@author: anand
"""
import matplotlib.pyplot as plt
import numpy as np
from data_diaphragm import *

def sigmaR(r, P, flatPlate):
    """
    Returns the radial stress in a membrane
    r: distance from the center of the diaphragm
    y0: maximum deflection
    diaphragm: diaphragm used
    """
    try:
        return 3/8 * P * flatPlate.a**2/ flatPlate.h**2 * ((3 + flatPlate.mu)* (r/flatPlate.a)**2 - (1 + flatPlate.mu))
    except ZeroDivisionError:
        return None
        

def sigmaT(r, y0, flatPlate):
    """
    Returns the tangential stress in flat plate
    r: distance from the center of the flat plate
    y0: maximum deflection
    diaphragm: diaphragm used
    """
    try:
        return 3/8 * P * flatPlate.a**2/ flatPlate.h**2 * ((3*flatPlate.mu + 1)* (r/flatPlate.a)**2 - (1 + flatPlate.mu))
    except ZeroDivisionError:
        return None

def maxSigmaR(P, flatPlate):
    """
    Returns maximum radial stress for given flat plate at given Pressure
    """
    return sigmaR(0, P, flatPlate)

def maxSigmaT(P, flatPlate):
    """
    Returns maximum tangential stress for a given flat plate at given Pressure
    """
    return sigmaT(0, P, flatPlate)

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

def flatPlateDeflect(r, P, flatPlate):
    """
    Returns the deflection for given flat plate with following parameters
    
    r: distace from the center of flat plate
    flatPlate: flatPlate used
    """
    return 3*(1- flatPlate.mu**2) * P / (16 * flatPlate.E * flatPlate.h**3) * (flatPlate.a**2 - r**2)**2


def detDeflect(P, flatPlate):
    """
    Returns a list of maximum values of deflection in mm for given applied pressure values
    
    P: list of pressure
    """
    return [flatPlateDeflect(0, p, flatPlate) for p in P]
    
def plotPvsy(P, flatPlate, legend):
    """
    Plots the graph of deflection variation with pressure variation for given flatPlate
    
    P: list of pressure values
    """
    y = detDeflect(P, flatPlate)
    graph(P, y, "Pressure[Pa]", "Deflection[m]", legend = legend)

if __name__ == "__main__":
    #plt.close("all") # close all previous figures
    P_max = 0.0005 * 10**5
    P = np.arange(0,P_max,P_max/1000.0)
    #Consideration of only tensile stresses
    plt.figure("Flat diaphragm:P vs. y using flat plate theory")
    plotPvsy(P, diaphNB40_50, "Diaphragm 40 and 50NB")
    plotPvsy(P, diaphNB15_20, "Diaphragm 15 and 20NB")
    plotPvsy(P, diaphNB25, "Diaphragm 25NB")
    