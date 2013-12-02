# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 16:55:40 2013

@author: anand
"""
import numpy as np
import matplotlib.pyplot as plt
from data_diaphragm import *

    
def tensileBendingDeflect(P, diaphragm, Kp = 1.0, Lp = 1.0):
    """
    Returns the deflection considering tensile as well as bending stresses for
    corrugated diaphragm.
    
    All parameters follow same system of units(SI).
    """
    coeff = np.zeros((len(P), 4))
    #coefficiet of y**3
    coeff[:,0] = Lp * diaphragm.Bp / diaphragm.h**3
    coeff[:,2] = Kp * diaphragm.Ap / diaphragm.h
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
    return diaphragm.E*diaphragm.h**4/diaphragm.a**4 * (diaphragm.Ap * y / diaphragm.h + diaphragm.Bp * y**3 / diaphragm.h**3)


    
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
    graph(P * 1e-5, deflect, "Pressure(bar)", "Deflection(mm)", legend = legend)


def sigmaTmax(diaphragm, P):
    """
    Returns the maximum tangential stress value for given pressure.
    
    P: Pressure applied[Pa] (can be a scalar or an array)
    """
    Ks = diaphragm.Ks
    return P * (diaphragm.a / diaphragm.h)**2 * Ks

def sigmaRmax(diaphragm, P):
    """
    Returns the maximum radial stress value for given pressure.
    
    P: Pressure applied[Pa] (can be a scalar or an numpy array)
    """
    q = diaphragm.q
    Kr = diaphragm.Kr
    return 9.0 * P * diaphragm.a**2 / ((q - 1) * (q + 3) * diaphragm.h**2) * Kr * (Kr + (0.1 * q * (q + 2) * diaphragm.l**2 / (3.0 * diaphragm.a)))

def extremeRadial(P, diaphragm):
    """
    Returns extreme radial stress for the corrugated diaphragm
    """
    lambda_ = 0.5 * diaphragm.l / diaphragm.a
    return 3 * P * diaphragm.a**2/((diaphragm.q + 3.)*diaphragm.h**2) * ((1 - lambda_)**3 - (1 - lambda_)**diaphragm.q)/((diaphragm.q - 3) * lambda_)
    
def plotPvssigmaT(P, diaphragm, legend):
    """
    Plots variation of maximum tangential stress with pressure
    
    P: Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    sigma_max = sigmaTmax(diaphragm, P)
    graph(P * 1e-5, sigma_max, "Pressure(bar)", "Maximum Tangential Stress[Pa]", legend = legend)

def plotPvssigmaR(P, diaphragm, legend):
    """
    Plots variation of maximum radial stress with pressure
    
    P: Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    sigma_max = sigmaRmax(diaphragm, P)
    graph(P * 1e-5, sigma_max, "Pressure(bar)", "Maximum Radial Stress[Pa]", legend = legend)

def plotPvsExtremeRadial(P, diaphragm, legend):
    """
    Plots variation of extreme radial stress with pressure
    
    P:Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    sigma_ext = extremeRadial(P, diaphragm)
    graph(P * 1e-5, sigma_ext, "Pressure[bar]", "Extreme Radial Stress[Pa]", legend = legend)

def plotyvssigmaR(P, diaphragm):
    """
    Plots variation of radial stress values with the deflection
    
    P: Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    deflection = tensileBendingDeflect(P, diaphragm) * 1e3
    sigma_max = sigmaRmax(diaphragm, P)
    graph(deflection, sigma_max, "Deflection[mm]", "Stress[Pa]", diaphragm.name + " maximum radial stress")

def plotyvssigmaT(P, diaphragm):
    """
    Plots variation of radial stress values with the deflection
    
    P: Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    deflection = tensileBendingDeflect(P, diaphragm) * 1e3
    sigma_max = sigmaTmax(diaphragm, P)
    graph(deflection, sigma_max, "Deflection[mm]", "Stress[Pa]", diaphragm.name + " maximum tangential stress")

def plotyvsExtremeRadial(P, diaphragm):
    """
    Plots variation of extreme radial stress with pressure
    
    P:Pressure [Pa] numpy array
    diaphragm: diaphragm used
    """
    deflection = tensileBendingDeflect(P, diaphragm) * 1e3
    sigma_ext = extremeRadial(P, diaphragm)
    graph(deflection, sigma_ext, "Deflection[mm]", "Stress[Pa]", diaphragm.name + " maximum extreme radial stress")
    
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
    graph(P * 1e-5, np.ones(len(P)) * diaphUsed.Syt, legend = "Tensile strength")
    plotPvssigmaR(P, diaphUsed, "Radial stress")
    plotPvsExtremeRadial(P, diaphUsed, "Extreme Radial Stress")
    plt.figure()
    plotyvsExtremeRadial(P, diaphUsed)
    plotyvssigmaR(P, diaphUsed)
    plotyvssigmaT(P, diaphUsed)
    plt.show()