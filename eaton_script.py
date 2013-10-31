import matplotlib.pyplot as plt
import numpy as np
from data_diaphragm import *

def Alpha(diaphragm):
    """
    Returns the factor alpha in the deflection formula
    """
    return 14 * (4 * diaphragm.h**2) / ((1+diaphragm.mu) * (23 - 9 * diaphragm.mu))

def D(diaphragm):
    """
    Returns the value of flexural rigidity for given diaphragm
    """
    return diaphragm.E * diaphragm.h**3 / (12 * (1 - diaphragm.mu**2))

def Beta(P, diaphragm):
    """
    Returns beta factor in deflection formula
    """
    return -7.0 * P * diaphragm.a**4 * diaphragm.h**2 / (8.0 * D(diaphragm) * (1 + diaphragm.mu) * (23 - 9.0 * diaphragm.mu))

def Gamma(P, diaphragm):
    """
    Returns the gamma factor for the given diaphragm
    """
    return (Alpha(diaphragm)**3 / 27.0 + Beta(P, diaphragm)**4 / 4.0)**(1/2.0)

def f(P, diaphragm):
    """
    Returns the maximum deflection for a given diaphragm
    """
    beta1 = Beta(P, diaphragm)
    gamma1 = Gamma(P, diaphragm)
    return ( - beta1 / 2.0 + gamma1)**(1/3.0) + (- beta1/ 2.0 - gamma1)**(1/3.0) 

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')

def detDeflect(P, diaphragm):
    """
    Returns a list of maximum values of deflection in mm for given applied pressure values
    
    P: list of pressure
    """
    return [f(p, diaphragm)*1e3 for p in P]
    
def plotPvsy(P, diaphragm, legend):
    """
    Plots the graph of deflection variation with pressure variation for given flatPlate
    
    P: list of pressure values
    """
    y = detDeflect(P, diaphragm)
    graph(P, y, "Pressure[Pa]", "Deflection[mm]", legend = legend)

if __name__ == "__main__":
    P_max = 4 * 10**5
    P = np.arange(0,P_max,P_max/1000.0 )
    plt.figure("Flat diaphragm:P vs. y using eaton manscript")
    plotPvsy(P, diaphNB40_50, "Diaphragm 40 and 50NB")
    plotPvsy(P, diaphNB15_20, "Diaphragm 15 and 20NB")
    plotPvsy(P, diaphNB25, "Diaphragm 25NB")
    plt.show()
