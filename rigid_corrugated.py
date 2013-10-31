# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:40:20 2013

@author: Anand
"""

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
    return (diaphragm.s / diaphragm.l * (1.5 * (diaphragm.H / diaphragm.h)**2 + 1))**0.5

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
    
def tensileBendingDeflect(P, diaphragm, Kp = 1, Lp = 1):
    """
    Returns the deflection considering tensile as well as bending stresses for
    corrugated diaphragm.
    
    All parameters follow same system of units(SI).
    """
    coeff = []
    #coefficiet of y**3
    coeff.append(calcBp(diaphragm) / diaphragm.h**3)
    coeff.append(0.0)
    coeff.append(calcAp(diaphragm) / diaphragm.h)
    coeff.append(-P * diaphragm.a**4 / (diaphragm.E * diaphragm.h**4))
    roots = np.roots(coeff)
    for root in roots:
        if root.imag == 0:
            return root.real

def plotPvsy(P, diaphragm, Kp, Lp, legend = "", color = ""):
    """
    Plots P vs y plot for corrugated diaphragm with rigid center
    Kp and Lp to be provided from graph
    """
    deflection = [tensileBendingDeflect(p, diaphragm, Kp, Lp) for p in P]
    graph(P, deflection, "Pressure[Pa]", "Deflection[mm]", legend, color)

def detDeflectTensile(P, diaphragm):
    """
    Returns the deflection for given list of pressures and for given diaphragm
    """
    return [tensileBendingDeflect(p, diaphragm) for p in P]

    
def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    
def plotPvsyTensileBending(P, diaphragm, legend):
    """
    Plots the pressure vs. deflection curve considering tensile and bending.
    
    P: list contaning variable pressures
    legend: legend for the plot
    """
    #diaphragm properties
    deflect = [tensileBendingDeflect(p, diaphragm) * 1e3 for p in P]
    graph(P, deflect, "Pressure(Pa)", "Deflection(mm)", legend = legend)
    
if __name__ == "__main__":
    plt.close("all")
    Pmax = 4e5
    P = np.arange(0, Pmax, Pmax/1000.0)
    #BPT corrugated diaphragm with rigid center
    diaphInUse = BPTCorrug_rigid
    print "q = ", calcq(diaphInUse)
    print "b/a = ", diaphInUse.b / diaphInUse.a
    deflection_rigid = np.arange(0, 2, 0.01)
    Kp = float(raw_input("Enter value of Kp for above q and b/a ratio: "))
    Lp = float(raw_input("Enter value of Lp for above q and b/a ratio: "))
    plotPvsy(P, diaphInUse, Kp, Lp, "BPT rigid diaphragm")
    #BPT corrugated diaphragm without rigid center
    diaphInUse = BPTCorrug
    plotPvsy(P, diaphInUse, 1, 1, "BPT without rigid center")
    
    plt.legend()
    plt.show()