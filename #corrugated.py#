# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 16:55:40 2013

@author: anand
"""
import numpy as np
import matplotlib.pyplot as plt
from data_diaphragm import *

def calcq(diaphragm):
    """
    Returns the value of profile factor for given corrugated diaphragm
    """
    return (1.5 * (diaphragm.H / diaphragm.h)**2 + 1)**0.5

def calcAp(diaphragm):
    """
    Returns the dimensionless stiffness coefficient for a given diaphragm
    """
    q = calcq(diaphragm)
    return 2*(3 + q)*(1 + q)/(3 * (1 - (diaphragm.mu/q)**2))

def calcBp(diaphragm):
    """
    Returns the value of dimensionless coefficient of nonlinear tension term
    for the given diaphragm
    """
    q = calcq(diaphragm)
    return 32.0 / (q**2 - 9) * (1.0/6  - (3 - diaphragm.mu)/((q - diaphragm.mu) * (q + 3)))
    
def tensileBendingDeflect(P, diaphragm, Kp = 1.0, Lp = 1.0):
    """
    Returns the deflection considering tensile as well as bending stresses for
    corrugated diaphragm.
    
    All parameters follow same system of units(SI).
    """
    coeff = np.zeros((len(P), 4))
    #coefficiet of y**3
    coeff[:,0] = Lp * calcBp(diaphragm) / diaphragm.h**3
    coeff[:,2] = Kp * calcAp(diaphragm) / diaphragm.h
    coeff[:,3] = -P * diaphragm.a**4 / (diaphragm.E * diaphragm.h**4)
    realRoot = np.zeros((len(P), 1))
    for i in range(len(P)):    
        roots = np.roots(coeff[i,:])
        for root in roots:
            if root.imag == 0:
                realRoot[i,0] = root.real
    return realRoot

def Pfromy(y, diaphragm):
    """
    Returns the pressure values from the respective defelction values
    """
    y = y*1e-3
    return diaphragm.E*diaphragm.h**4/diaphragm.a**4 * (calcAp(diaphragm) * y / diaphragm.h + calcBp(diaphragm) * y**3 / diaphragm.h**3)


    
def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    plt.grid()
    
def plotPvsyTensileBending(P, diaphragm, legend):
    """
    Plots the pressure vs. deflection curve considering tensile and bending.
    
    P: list contaning variable pressures
    legend: legend for the plot
    """
    #diaphragm properties
    deflect = tensileBendingDeflect(P, diaphragm) * 1e3
    graph(P, deflect, "Pressure(Pa)", "Deflection(mm)", legend = legend)

def calcKs(diaphragm):
    """
    Returns the factor Ks required for determination of maximum tangential stress
    
    diaphragm: a couugated diaphragm used
    """
    q = calcq(diaphragm)
    return (3 + np.sqrt(6 * (q**2  - 1)))/((q - 1)*(q + 3)) * (2.0 / (q - 1))**(2.0 / (q -3))

def calcKr(diaphragm):
    """
    Returns the factor Kr required for determination of maximum radial stress
    diaphragm: corrugated diaphragm used
    """
    q = calcq(diaphragm)
    return (6.0/(q * (q -1)))**(1.0 / (q -3))

def sigmaTmax(diaphragm, P):
    """
    Returns the maximum tangential stress value for given pressure.
    
    P: Pressure applied[Pa] (can be a scalar or an array)
    """
    Ks = calcKs(diaphragm)
    return P * (diaphragm.a / diaphragm.h)**2 * Ks

def sigmaRmax(diaphragm, P):
    """
    Returns the maximum radial stress value for given pressure.
    
    P: Pressure applied[Pa] (can be a scalar or an numpy array)
    """
    q = calcq(diaphragm)
    Kr = calcKr(diaphragm)
    return 9.0 * P * diaphragm.a**2 / ((q - 1) * (q + 3) * diaphragm.h**2) * Kr * (Kr + (0.1 * q * (q + 2) * diaphragm.l**2 / (3.0 * diaphragm.a)))

def plotPvssigmaT(P, diaphragm, legend):
    """
    Plots variation of maximum tangential stress with pressure
    
    P: Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    sigma_max = sigmaTmax(diaphragm, P)
    graph(P, sigma_max, "Pressure(Pa)", "Maximum Tangential Stress[Pa]", legend = legend)

def plotPvssigmaR(P, diaphragm, legend):
    """
    Plots variation of maximum tangential stress with pressure
    
    P: Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    sigma_max = sigmaRmax(diaphragm, P)
    graph(P, sigma_max, "Pressure(Pa)", "Maximum Radial Stress[Pa]", legend = legend)
    
if __name__ == "__main__":
    plt.close("all")
    P_max = 1e5
    P = np.arange(0,P_max + P_max / 1000.0,P_max/1000.0 )
    #considering of tensile and bending stresses
    plt.figure("Flat diaphragm:P vs. y(tensile + bending) for corrugated diaphragm")
#    plotPvsyTensileBending(P, diaphNB40_50_corrug, "Diaphragm 40 and 50NB")
#    plotPvsyTensileBending(P, diaphNB15_20_corrug, "Diaphragm 15 and 20NB")
#    plotPvsyTensileBending(P, diaphNB25_corrug, "Diaphragm 25NB")
#    plt.title("Pressure vs deflection considering tensile and bending for corrugated diaphragm")
#    plt.figure("BPT capsule")
#    plotPvsyTensileBending(P, BPTCorrug, "BPT diaphragm")
#    deflection = np.arange(0, 2.5, 0.1)
#    #plt.plot(Pnew, deflection, 'ro',label = "BPT diaphragm direct method")
#    plt.figure("Previously manufactured corrugated diaphragm")
#    plt.title("Pressure vs deflection considering tensile and bending for corrugated diaphragm")\
    diaphUsed = premade_corrug
    plotPvsyTensileBending(P, diaphUsed, "Previously manufactured")
    plt.figure("Pressure vs stress")
    plotPvssigmaT(P, diaphUsed, "Tangential stress")
    graph(P, np.ones(len(P)) * diaphUsed.Syt, legend = "Tensile strength")
    plotPvssigmaR(P, diaphUsed, "Radial stress")
    plt.show()