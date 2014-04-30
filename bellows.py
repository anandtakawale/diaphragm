# -*- coding: utf-8 -*-
"""
Created on Mon Dec 02 14:16:35 2013

@author: Anand
"""
import matplotlib.pyplot as plt
import numpy as np
import data_diaphragm
from roark_membrane import sigmaRmax, sigmaEdge

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    plt.grid()

def tensileBendingDeflect(P, diaphragm):
    """
    Returns the deflection considering tensile as well as bending stresses
    
    P:Pressure in [Pa] numpy array
    
    All parameters follow same system of units(SI).
    """
    coeff = np.zeros((len(P), 4))
    #coefficiet of y**3
    coeff[:,0] = diaphragm.Bp / diaphragm.h**3
    #coefficient of y**2 is already made zero
    #coefficient of y
    coeff[:,2] = 1.0/ (diaphragm.Ap * diaphragm.h)
    #coefficient constant
    coeff[:,3] = -P * diaphragm.a**4 / (diaphragm.E * diaphragm.h**4)
    realRoot = np.zeros((len(P), 1))
    for i in range(len(P)):
        roots = np.roots(coeff[i,:])
        for root in roots:
            if root.imag == 0:
                realRoot[i,0] = root.real
    return realRoot

def forceDeflect(F, diaphragm):
    """
    Returns the amount of deflection of the diaphragm when applied by force F
    
    Note: This is to be used when deflections are comparable to thickness of the diaphragm
    """
    return diaphragm.Af * F * diaphragm.a**2.0/ (diaphragm.E * diaphragm.h**3.0)

def plotForcevsy(F, bellows, legend, color= ""):
    """
    Plots the force vs deflection curve for bellows
    """
    if bellows.__class__.__name__ == 'Bellows':
        deflect = forceDeflect(F, bellows) * 1e3 * bellows.n
    else:
        deflect = forceDeflect(F, bellows) * 1e3
    graph(F, deflect, "Force[N]", "Deflection[mm]", legend, color)
    
def plotPvsyTensileBending(P, bellows, legend, color = ""):
    """
    Plots the pressure vs. deflection curve considering tensile and bending.
    
    P: list contaning variable pressures
    legend: legend for the plot
    """
    #diaphragm properties
    if bellows.__class__.__name__ == 'Bellows':
        deflect = tensileBendingDeflect(P, bellows) * 1e3 * bellows.n
    else:
        deflect = tensileBendingDeflect(P, bellows) * 1e3
    graph(P * 1e-5, deflect, "Pressure[bar]", "Deflection[mm]", legend, color)
    
def sigma(P, diaphragm):
    """
    Returns maximum radial stress developed in the diaphragm for given pressure
    
    THIS FORMULA IS TO BE USED ONLY FOR SMALL DEFLECTION i.e deflection_max / thickness > 5
    """
    
    return 3.0 * P /(4.0 * diaphragm.h**2) * (diaphragm.a**2 - diaphragm.b**2)
    

def plotPvssigma(P, diaphragm, legend):
    sigmar = sigma(P, diaphragm)
    plt.plot([0, max(P) * 1e-5], [diaphragm.Syt * 1e-6, diaphragm.Syt * 1e-6], label = "Yield stress")
    plt.plot([0, max(P) * 1e-5], [diaphragm.Sut * 1e-6, diaphragm.Sut * 1e-6], label = "Tensile strength")
    graph(P * 1e-5, sigmar * 1e-6, xlabel = "Pressure[bar]", ylabel = "Stress[MPa]" ,legend = legend)
    
if __name__ == "__main__":
    P_max = 2e5
    P = np.arange(0, P_max + P_max/1000.0, P_max/1000.0)
    plt.close('all')
#    plt.figure()
#    plotPvsyTensileBending(P, data_diaphragm.BT6diaph, data_diaphragm.BT6diaph.name)
#    plt.figure()
#    plotPvsyTensileBending(P, data_diaphragm.BT6Bellow, data_diaphragm.BT6Bellow.name)
#    plt.plot([0, P_max * 1e-5], [1.0, 1.0], label = "Deflection of 1mm")
#    plotPvsyTensileBending(P, data_diaphragm.BT6Bellow_hastealloy, data_diaphragm.BT6Bellow_hastealloy.name)
#    plt.figure()
#    plotPvsyTensileBending(P, data_diaphragm.minami_bellow, data_diaphragm.minami_bellow.name)
#    plt.figure()
#    plotPvssigma(P, data_diaphragm.BT6diaph, data_diaphragm.BT6diaph.name)
#    plt.figure()
#    plotPvssigma(P, data_diaphragm.minami_advice, data_diaphragm.minami_advice.name)
#    plt.figure()
#    F_max = 5e1 # 50N of maximum force
#    F = np.linspace(0, F_max, 1001)
#    plt.plot([  0.     ,   5.2974 ,  11.42865,  24.525  ], [0, 0.5,1,1.5], "o-")
#    F_bt2 = np.array([0, 0.055, .225, .5, .810,1.13, 1.445, 1.825])
#    y_bt2 = np.array([0,0.09, 0.26, 0.5, 0.76, 1.02, 1.25, 1.5])
#    graph(F_bt2 * 9.81 , y_bt2, "Force[N]", "Deflection[mm]","BT6 spirax bellow sample 2", 'o-')
#    plotForcevsy(F, data_diaphragm.BT6Bellow, data_diaphragm.BT6Bellow.name)
#    plt.plot([0, F_max], [2.0, 2.0])
#    plt.figure("Kuze K1630 P vs y")
#    plotPvsyTensileBending(P, data_diaphragm.K1630_bellow, "Kuze K1630")
#    plt.figure("Kuze K1630 P vs Stress")
#    plotPvssigma(P, data_diaphragm.K1630_bellow, "K1630")
    plt.figure()
    plotPvsyTensileBending(P, data_diaphragm.BT6diaph, data_diaphragm.BT6diaph.name)
    plt.show()