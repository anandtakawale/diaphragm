# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:15:47 2013

@author: anand
"""
import matplotlib.pyplot as plt
import numpy as np
from data_diaphragm import *

def sigmaR(r, y0, diaphragm):
    """
    Returns the radial stress in a membrane
    r: distance from the center of the diaphragm
    y0: maximum deflection
    diaphragm: diaphragm used
    """
    try:
        return diaphragm.E * y0**2 /(4.0 * diaphragm.a**2) * ((3.0 - diaphragm.mu)/(1.0 - diaphragm.mu) - (r/diaphragm.a)**2)
    except ZeroDivisionError:
        return None
        

def sigmaT(r, y0, diaphragm):
    """
    Returns the tangential stress in membrane
    r: distance from the center of the diaphragm
    y0: maximum deflection
    diaphragm: diaphragm used
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
    plt.grid()
    #plt.xticks(np.arange(0, max(x), max(x)/10.0))
    

def tensileDeflect(P, diaphragm):
    """
    Returns the deflection considering only for tensile stresses
    using given parameters.
    
    All parameters follow same system of units(SI).
    """
    if isShear(diaphragm):
        raise ValueError("Shear stresses need to be considered")
    else:
        return (P * diaphragm.a**4 / (diaphragm.E * diaphragm.h**4) * (3.0 * (1 - diaphragm.mu)) / (7.0 - diaphragm.mu))**(1/3.0) * diaphragm.h
    
def plotPvsyTensile(P, diaphragm, legend, color = ""):
    """
    Plots the pressure vs. deflection curve considering tensile.
    
    P: list contaning variable pressures
    E: Youngs modulus
    a: radius of plate
    h: thickness of plate
    mu: Poisson ratio
    
    """
    #diaphragm properties
    deflect = tensileBendingDeflect(P, diaphragm)
    graph(P * 1e-5, deflect, "Pressure(Pa)", "Deflection(mm)", legend, color)

def plotPvsyTensileBending(P, diaphragm, legend, color = ""):
    """
    Plots the pressure vs. deflection curve considering tensile and bending.
    
    P: list contaning variable pressures
    legend: legend for the plot
    """
    #diaphragm properties
    deflect = tensileBendingDeflect(P, diaphragm) * 1e3
    graph(P * 1e-5, deflect, "Pressure(Pa)", "Deflection(mm)", legend, color)
    
def plotPvssigmaR(P, diaphragm, legend):
    """
    Plots variation of maximum radial stress with pressure
    """
    #maximum deflection for given pressure
    deflect = tensileBendingDeflect(P, diaphragm)
    sigma_max = [sigmaRmax(y, diaphragm) for y in deflect]
    graph([p * 1e-5 for p in P], sigma_max, "Pressure(Pa)", "Radial Stress(Pa)", legend = legend)
    sigma_allow = [maxShear(diaphragm) for x in range(len(P))]
    graph([p * 1e-5 for p in P], sigma_allow, "Pressure(Pa)", "Radial Stress(Pa)", legend = "Maximum allowable")
    
def plotPvssigmaT(P, diaphragm, legend):
    """
    Plots variation of maximum tangential stress with pressure
    """
    #maximum deflection for given pressure
    deflect = tensileBendingDeflect(P, diaphragm)
    sigma_max = [sigmaTmax(y, diaphragm) for y in deflect]
    graph([p * 1e-5 for p in P], sigma_max, "Pressure(Pa)", "Tangential Stress(Pa)", legend = legend)
    
def tensileBendingDeflect(P, diaphragm):
    """
    Returns the deflection considering tensile as well as bending stresses
    
    P:Pressure in [Pa] numpy array
    
    All parameters follow same system of units(SI).
    """
    coeff = np.zeros((len(P), 4))
    #coefficiet of y**3
    coeff[:,0] = (7.0 - diaphragm.mu) / (3.0 * (1.0 - diaphragm.mu)) / diaphragm.h**3
    #coefficient of y**2 is already made zero
    #coefficient of y
    coeff[:,2] = 16.0 / (3 * (1 - diaphragm.mu**2)) / diaphragm.h
    #coefficient constant
    coeff[:,3] = -P * diaphragm.a**4 / (diaphragm.E * diaphragm.h**4)
    realRoot = np.zeros((len(P), 1))
    for i in range(len(P)):
        roots = np.roots(coeff[i,:])
        for root in roots:
            if root.imag == 0:
                realRoot[i,0] = root.real
    return realRoot
    
def isShear(diaphragm):
    """
    Returns True if shear stresses need to be considered
    i.e when h/a > 0.15
    """
    return diaphragm.h/float(diaphragm.a) > 0.15
    
def calcfs(Syt, sigma_max):
    """
    Returns the factor of safety for a given plate.

    Syt: Yield strength of material
    sigma_max: maximum stress in the element
    """
    return maxShear(diaphragm)/sigma_max

def sigmaRmax(y0, diaphragm):
    """
    Returns the maximum radial stress for given parameters.
    
    For membrane/flat plate the maximum value occurs at the centre of the
    plate i.e at r = 0.0
    """
    return sigmaR(0.0, y0, diaphragm)
    
def sigmaTmax(y0, diaphragm):
    """
    Returns the maximum tangential stress for given parameters.
    
    For membrane/flat plate the maximum value occurs at the centre of the
    plate i.e at r = 0.0
    """
    return sigmaT(0, y0, diaphragm)
    
def maxShear(diaphragm):
    """
    Returns maximum shear stress from yield strength of material.
    
    Using maximum shear stress theory
    """
    return diaphragm.Syt / 2.0

def calcMaxStress(P, diaphragm):
    """
    Returns the maximum radial stress when a pressure is applied to the
    membrane with given dimensions and properties
    
    """
    #calculating deflection
    y = tensileBendingDeflect(P, diaphragm)
    return sigmaRmax(y, diaphragm)

def plotyvssigmaR(P, diaphragm):
    """
    Plots the variation of maximum radial stress with deflection
    """
    deflection = tensileBendingDeflect(P, diaphragm)
    sigma_max = sigmaRmax(deflection, diaphragm)
    deflection = deflection * 1e3
    graph(deflection, sigma_max, "Deflection[mm]", "Stress[Pa]", diaphragm.name + "Max radial stress")

def plotyvssigmaT(P, diaphragm):
    """
    Plots the variation of maximum radial stress with deflection
    """
    deflection = tensileBendingDeflect(P, diaphragm)
    sigma_max = sigmaTmax(deflection, diaphragm)
    deflection = deflection * 1e3
    graph(deflection, sigma_max, "Deflection[mm]", "Stress[Pa]", diaphragm.name + "Max tangential stress")

    
if __name__ == '__main__':
    #close all previous figures
    plt.close('all')
