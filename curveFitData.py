# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:03:37 2013

@author: Admin
"""

import readout
import matplotlib.pyplot as plt
from data_diaphragm import *
import numpy as np
from scipy.optimize import curve_fit
import membrane
import roark_membrane

def func(y, c1, c2):
    return c1 * y + c2 * y**3.0
    
def funcinv(P, diaphragm, c1, c2):
    """
    Returns the value for the deflection for a given pressure by solving
    nonlinear equation in terms of y
    """
    coeff = np.zeros((len(P), 4))
    coeff[:, 0] = c2
    coeff[:, 2] = c1
    coeff[:, 3] = -P
    realRoot = np.zeros(len(P))
    for i in range(len(P)):    
        roots = np.roots(coeff[i,:])
        for root in roots:
            if root.imag == 0:
                realRoot[i] = float(root.real)
    return realRoot

def curveFit(f, xdata, ydata, diaphragm):
    """
    Plots the data along with the corresponding curve using sympy
    
    f: function to which data is to be fitted
    xdata: dependent variable values
    ydata: independent variable values
    diaphragm: diaphragm used for experimentation
    """
    popt, pcov = curve_fit(f, xdata, ydata)
    ymax = 5
    y = np.arange(0, ymax, ymax/1000.0)
    P = f(y * 1e-3, popt[0], popt[1])
    plt.plot(P, y, label = "c1 = " + str(popt[0]) + "\nc2 = " + str(popt[1]))
    plt.legend(loc = 'best')
    #plotting analytical curve using handbook equations
    membrane.plotPvsyTensileBending(P, diaphragm, "Handbook equations")
    #plotting analytical curve using Roarks formulae
    roark_membrane.plotPvsy(P, diaphragm, "Roarks equations")
    #using analytical results in handbook
    c1 = diaphragm.E * diaphragm.h**3 / diaphragm.a**4 * 16.0 / (3 * (1 - diaphragm.mu**2))
    c2 = diaphragm.E * diaphragm.h /diaphragm.a**4 * (7 - diaphragm.mu)/(3 * (1 - diaphragm.mu))
    print "\nUsing analytical calculations\nc1 = " + str(c1) + "\nc2 = " + str(c2)
    print "\nUsing curve fitting to experimental data\nc1 = " + str(popt[0]) + "\nc2 = " + str(popt[1])
    return popt

def relativeErr(theory, expt):
    """
    Determines the relative error between the theoretical and experimental values
    
    theory: Theoretical values numpy array
    expt: Experimental values numpy array
    """
    return np.divide(np.subtract(theory, expt), theory) * 1e2
    
    
if __name__ == "__main__":
     plt.close('all')
     P = np.array(readout.readout("../expt/Pvsy/curvefitdata_single_upto3kgcm2.xls", 0, 0)) * 9.81e4
     y = np.array(readout.readout("../expt/Pvsy/curvefitdata_single_upto3kgcm2.xls", 0, 1))
     plt.plot(P, y, 'o')
     plt.title("Pressure vs deflection")
     c1, c2= curveFit(func, y * 1e-3, P, diaphNB40_50)
     
     #calculating and plotting percent relative error
     Pmax = 4e5
     P = np.arange(0, Pmax, Pmax/1000)
     y_analytical = np.array(membrane.detDeflectTensile(P, diaphNB40_50))
     y_curvefit = funcinv(P, diaphNB40_50, c1, c2) 
     error = relativeErr(y_analytical, y_curvefit)
     plt.figure()
     membrane.graph(P, error, "Pressure[Pa]", "Percent relative error", "Percent relative error between theoretical and analytical")
     plt.grid()
     plt.show()

    
#==============================================================================
#     diphUsed = diaphNB40_50_double
#     P = np.array(readout.readout("../expt/Pvsy/curvefitdata_double_upto4bar.xls", 0, 0)) * 1e5
#     y = np.array(readout.readout("../expt/Pvsy/curvefitdata_double_upto4bar.xls", 0, 1))
#     plt.plot(P, y, 'o')
#     plt.title("Pressure vs deflection")
#     c1, c2= curveFit(func, y * 1e-3, P, diphUsed)
#     
#     #calculating and plotting percent relative error
#     Pmax = 4e5
#     P = np.arange(0, Pmax, Pmax/1000)
#     y_analytical = np.array(membrane.detDeflectTensile(P, diphUsed))
#     y_curvefit = funcinv(P, diphUsed, c1, c2) 
#     error = relativeErr(y_analytical, y_curvefit)
#     plt.figure()
#     membrane.graph(P, error, "Pressure[Pa]", "Percent relative error", "Percent relative error between theoretical and analytical")
#==============================================================================