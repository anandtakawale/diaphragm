# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 15:09:23 2013

@author: Anand
"""

import matplotlib.pyplot as plt
from data_diaphragm import *

def sigmaR(r, y0, diaphragm):
    """
    Returns the radial stress in a membrane
    
    r:Distance from the center of the diaphragm
    y0: Maximum deflection
    diaphragm: Diaphragm used
    """
    try:
        return diaphragm.E * y0**2 /(4.0 * diaphragm.a**2) * ((3.0 - diaphragm.mu)/(1.0 - diaphragm.mu) - (r/diaphragm.a)**2)
    except ZeroDivisionError:
        return None
        

def sigmaT(r, y0, diaphragm):
    """
    Returns the tangential stress in membrane

    r:Distance from the center of the diaphragm
    y0: Maximum deflection
    diaphragm: Diaphragm used    
    """
    try:
        return diaphragm.E * y0**2 /(4.0 * diaphragm.a**2) * ((3.0 - diaphragm.mu)/(1.0 - diaphragm.mu) - 3.0 * (r/diaphragm.a)**2)
    except ZeroDivisionError:
        return None

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    
def calcBp(diaphragm):
    """
    Returns value of tensile coefficient Bp
    
    diaphragm: Diaphragm used
    """
    return ((7.0 - diaphragm.mu)/3.0 * (1 + (diaphragm.b/diaphragm.a)**2  + (diaphragm.b/diaphragm.a)**4) +\
    (3 - diaphragm.mu)**2 / (1 + diaphragm.mu) * (diaphragm.b/diaphragm.a)**2)/(1- diaphragm.mu) / (1 - (diaphragm.b/diaphragm.a)**4) / (1 - (diaphragm.b/diaphragm.a)**2)**2

def plotBp(mu = []):
    """
    Plots the graph for stiffness coefficient variation with b/a ratio
    """
    plt.figure()
    for val in mu:
        bbya = [x * 0.001 for x in range(400,900)]
        Bp = [calcBp(1.0, var, val) for var in bbya]
        graph(bbya, Bp, "b/a", "Bp", legend = "mu = %s" %val)
    plt.show()
    
def plotPvsy(P, diaphragm, legend):
    """
    Plots the pressure vs. deflection curve for given parameters
    
    P: list contaning variable pressures
    legend: Legend to be given to plot
    """
    deflect = [rigidCentreDeflect(p, diaphragm) * 10.0**3 for p in P]
    plt.title("Pressure deflection curve for diaphragm")
    graph(P, deflect, "Pressure(Pa)", "Deflection(mm)", legend = legend)
    
def detDeflectTensile(P, diaphragm):
    """
    Returns the deflection for given list of pressures and for given diaphragm

    P: List of applied pressure
    """
    return [rigidCentreDeflect(p, diaphragm) for p in P]
    
def rigidCentreDeflect(P, diaphragm):
    """
    Returns the deflection of membrane with rigid centre.
    
    All parameters follow same system of units(SI).
    """
    if isShear(diaphragm):
        raise ValueError("Shear stresses need to be considered")
    Bp = calcBp(diaphragm)
    return (P * diaphragm.a**4 / ((diaphragm.E * diaphragm.h) * Bp))**(1.0/3)
    
def isShear(diaphragm):
    """
    Returns True if shear stresses need to be considered
    i.e when h/a > 0.15
    """
    return diaphragm.h/float(diaphragm.a) > 0.15
    
def calcfs(diaphragm, sigma_max):
    """
    Returns the factor of safety for a given plate.
    
    sigma_max: Maximum stress present in the diaphragm
    """
    return maxShear(diaphragm.Syt)/sigma_max

def sigmaRmax(y0, diaphragm):
    """
    Returns the maximum radial stress for given parameters.
    
    For membrane/flat plate the maximum value occurs at the centre of the
    plate i.e at r = 0.0
    """
    return sigmaR(0, y0, diaphragm)
    
def maxShear(diaphragm):
    """
    Returns maximum shear stress from yield strength of material.
    Using maximum shear stress theory.
    """
    return diaphragm.Syt / 2.0

def calcMaxStress(P, r, diaphragm):
    """
    Returns the maximum radial stress when a pressure is applied to the
    membrane with given dimensions and properties
    
    """
    #calculating deflection
    y = rigidCentreDeflect(P, diaphragm)
    return sigmaRmax(y, diaphragm)
    
def plotPvssigmaR(P, diaphragm, legend):
    """
    Plots variation of maximum radial stress with pressure
    """
    #maximum deflection for given pressure
    deflect = detDeflectTensile(P, diaphragm)
    sigma_max = [sigmaRmax(y, diaphragm) for y in deflect]
    graph(P, sigma_max, "Pressure(Pa)", "Radial Stress(Pa)", legend = legend)  
    

    
    
